"""
Google Cloud Vision AI Engine for Restaurant Inspection
Uses Google Cloud Vision API for accurate object detection
"""
import os
from google.cloud import vision
from typing import Dict, Any
import io


class InspectionAIEngine:
    """AI Engine using Google Cloud Vision API"""
    
    def __init__(self):
        """Initialize Google Cloud Vision client"""
        import json
        import tempfile
        
        # Check for environment variable (Render deployment)
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if credentials_json:
            # Production: Create temporary file from environment variable
            print("Using credentials from environment variable")
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                f.write(credentials_json)
                credentials_path = f.name
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        else:
            # Development: Use local file
            print("Using local credentials file")
            credentials_path = r"C:\Users\ahmad\restaurant-inspection-484615-ba2b3b137624.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        # Initialize Vision API client
        self.client = vision.ImageAnnotatorClient()
        print("Google Cloud Vision AI Engine initialized successfully")
    
    def analyze_inspection(self, image_paths: Dict[str, str]) -> Dict[str, Any]:
        """
        Main analysis function using Google Cloud Vision API
        Analyzes all 6 images and returns results
        """
        print("="*50)
        print("Starting Vision API Analysis...")
        print("="*50)
        
        results = {
            "overall_status": "compliant",
            "overall_score": 0,
            "criteria": []
        }
        
        # Criterion 1: Exposed Wires/Cables (3 images)
        print("\n[1/4] Checking for exposed wires...")
        criterion1 = self.check_exposed_wires({
            "ceiling": image_paths["ceiling"],
            "wall": image_paths["wall"],
            "floor": image_paths["floor_general"]
        })
        results["criteria"].append(criterion1)
        
        # Criterion 2: AC Units on Facade (1 image)
        print("\n[2/4] Checking for AC units...")
        criterion2 = self.check_ac_units(image_paths["facade"])
        results["criteria"].append(criterion2)
        
        # Criterion 3: Floor Joints (1 image)
        print("\n[3/4] Checking floor joints...")
        criterion3 = self.check_floor_joints(image_paths["floor_prep"])
        results["criteria"].append(criterion3)
        
        # Criterion 4: Lighting Adequacy (1 image)
        print("\n[4/4] Checking lighting...")
        criterion4 = self.check_lighting(image_paths["lighting"])
        results["criteria"].append(criterion4)
        
        # Calculate overall score
        total_score = sum([c["score"] for c in results["criteria"]])
        results["overall_score"] = round(total_score / len(results["criteria"]), 1)
        
        # Determine overall status
        if results["overall_score"] >= 90:
            results["overall_status"] = "compliant"
        elif results["overall_score"] >= 70:
            results["overall_status"] = "needs_improvement"
        else:
            results["overall_status"] = "non_compliant"
        
        print("\n" + "="*50)
        print(f"Analysis Complete! Overall Score: {results['overall_score']}")
        print("="*50)
        
        return results
    
    def _detect_objects_in_image(self, image_path: str) -> Dict[str, Any]:
        """Detect objects in image using Vision API (optimized batch request)"""
        try:
            print(f"Analyzing image: {image_path}")
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Use batch annotate for all features in one call
            features = [
                vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION, max_results=10),
                vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES),
                vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION, max_results=10),
            ]
            
            request = vision.AnnotateImageRequest(image=image, features=features)
            response = self.client.annotate_image(request=request)
            
            print(f"✓ Image analyzed successfully")
            
            return {
                "objects": [(obj.name, obj.score) for obj in response.localized_object_annotations],
                "labels": [(label.description, label.score) for label in response.label_annotations],
                "properties": response.image_properties_annotation
            }
        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            return {"objects": [], "labels": [], "properties": None}
    
    def check_exposed_wires(self, images: Dict[str, str]) -> Dict[str, Any]:
        """Check for exposed wires/cables using Vision API"""
        results = {
            "criterion_id": 1,
            "criterion_name": "الأسلاك والأنابيب الظاهرة",
            "criterion_name_en": "Exposed Wires and Pipes",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {},
            "images_analyzed": 3
        }
        
        violations_found = False
        confidences = []
        
        for location, img_path in images.items():
            detection = self._detect_objects_in_image(img_path)
            
            # Check for wire/cable related objects
            wire_keywords = ['cable', 'wire', 'cord', 'pipe', 'tube', 'conduit', 'wiring']
            found_wires = []
            
            for obj_name, score in detection["objects"]:
                if any(keyword in obj_name.lower() for keyword in wire_keywords):
                    found_wires.append((obj_name, score))
                    violations_found = True
            
            for label, score in detection["labels"]:
                if any(keyword in label.lower() for keyword in wire_keywords):
                    if label not in [f[0] for f in found_wires]:
                        found_wires.append((label, score))
                        violations_found = True
            
            confidence = max([score for _, score in found_wires], default=0.85)
            confidences.append(confidence)
            
            results["details"][location] = {
                "has_exposed_wires": len(found_wires) > 0,
                "confidence": float(confidence),
                "description": f"تم اكتشاف {len(found_wires)} عنصر مشبوه" if found_wires else "لا توجد أسلاك ظاهرة",
                "detected_items": [name for name, _ in found_wires]
            }
        
        if violations_found:
            results["status"] = "non_compliant"
            results["score"] = 40
        else:
            results["status"] = "compliant"
            results["score"] = 95
        
        results["confidence"] = float(sum(confidences) / len(confidences))
        return results
    
    def check_ac_units(self, image_path: str) -> Dict[str, Any]:
        """Check for AC units on facade using Vision API"""
        results = {
            "criterion_id": 2,
            "criterion_name": "وحدات التكييف على الواجهة",
            "criterion_name_en": "AC Units on Facade",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {}
        }
        
        detection = self._detect_objects_in_image(image_path)
        
        # Check for AC unit related objects
        ac_keywords = ['air conditioner', 'ac unit', 'hvac', 'cooling unit', 'condenser']
        found_ac_units = []
        
        for obj_name, score in detection["objects"]:
            if any(keyword in obj_name.lower() for keyword in ac_keywords):
                found_ac_units.append((obj_name, score))
        
        for label, score in detection["labels"]:
            if any(keyword in label.lower() for keyword in ac_keywords):
                if label not in [f[0] for f in found_ac_units]:
                    found_ac_units.append((label, score))
        
        ac_count = len(found_ac_units)
        confidence = max([score for _, score in found_ac_units], default=0.90)
        
        results["details"]["facade"] = {
            "has_ac_units": ac_count > 0,
            "unit_count": ac_count,
            "confidence": float(confidence),
            "description": f"تم اكتشاف {ac_count} وحدة تكييف على الواجهة" if ac_count > 0 else "لا توجد وحدات تكييف ظاهرة",
            "detected_units": [name for name, _ in found_ac_units]
        }
        
        if ac_count > 0:
            results["status"] = "non_compliant"
            results["score"] = 30
        else:
            results["status"] = "compliant"
            results["score"] = 98
        
        results["confidence"] = float(confidence)
        return results
    
    def check_floor_joints(self, image_path: str) -> Dict[str, Any]:
        """Check for floor joints/cracks using Vision API"""
        results = {
            "criterion_id": 3,
            "criterion_name": "الأرضيات بدون فواصل",
            "criterion_name_en": "Seamless Flooring",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {}
        }
        
        detection = self._detect_objects_in_image(image_path)
        
        # Check for floor defects
        defect_keywords = ['crack', 'gap', 'joint', 'seam', 'grout line', 'tile']
        found_defects = []
        
        for label, score in detection["labels"]:
            if any(keyword in label.lower() for keyword in defect_keywords):
                found_defects.append((label, score))
        
        defect_count = len(found_defects)
        confidence = 0.85
        
        results["details"]["floor"] = {
            "has_joints": defect_count > 3,
            "joint_count": defect_count,
            "confidence": float(confidence),
            "description": f"تم اكتشاف {defect_count} عيب محتمل" if defect_count > 3 else "الأرضية موحدة",
            "detected_issues": [name for name, _ in found_defects]
        }
        
        if defect_count > 5:
            results["status"] = "non_compliant"
            results["score"] = 50
        elif defect_count > 3:
            results["status"] = "needs_improvement"
            results["score"] = 75
        else:
            results["status"] = "compliant"
            results["score"] = 92
        
        results["confidence"] = float(confidence)
        return results
    
    def check_lighting(self, image_path: str) -> Dict[str, Any]:
        """Check lighting adequacy using Vision API"""
        results = {
            "criterion_id": 4,
            "criterion_name": "كفاية الإضاءة",
            "criterion_name_en": "Lighting Adequacy",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {}
        }
        
        detection = self._detect_objects_in_image(image_path)
        
        # Analyze image properties for brightness
        try:
            if detection["properties"] and detection["properties"].dominant_colors:
                colors = detection["properties"].dominant_colors.colors
                # Calculate average brightness from dominant colors
                avg_brightness = sum([c.pixel_fraction * (c.color.red + c.color.green + c.color.blue) / 3 
                                    for c in colors[:3]]) / sum([c.pixel_fraction for c in colors[:3]])
                
                brightness_percent = int((avg_brightness / 255) * 100)
                is_adequate = avg_brightness > 100
            else:
                # Fallback to label detection
                lighting_labels = [label for label, score in detection["labels"] 
                                 if 'light' in label.lower() or 'bright' in label.lower()]
                is_adequate = len(lighting_labels) > 0
                brightness_percent = 75
                avg_brightness = 150
        except:
            is_adequate = True
            brightness_percent = 75
            avg_brightness = 150
        
        results["details"]["lighting"] = {
            "brightness_level": float(avg_brightness),
            "is_adequate": is_adequate,
            "confidence": 0.88,
            "description": f"مستوى الإضاءة جيد ({brightness_percent}%)" if is_adequate else f"مستوى الإضاءة ضعيف ({brightness_percent}%)"
        }
        
        if not is_adequate:
            results["status"] = "non_compliant"
            results["score"] = 55
        else:
            results["status"] = "compliant"
            results["score"] = 90
        
        results["confidence"] = 0.88
        return results
