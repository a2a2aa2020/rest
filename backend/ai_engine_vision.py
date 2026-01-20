"""
Google Cloud Vision AI Engine for Restaurant Inspection
Uses Google Cloud Vision API and Gemini Vision for accurate object detection
"""
import os
from google.cloud import vision
from typing import Dict, Any
import io
import json
from google import genai



class InspectionAIEngine:
    """AI Engine using Google Cloud Vision API"""
    
    def __init__(self):
        """Initialize Google Cloud Vision and Gemini Vision clients"""
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
        
        # Initialize Gemini Vision
        try:
            gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCC-Xr3nLr9zB40xMwWdfb_dh5cEmsbQeI')  # New project key
            self.gemini_client = genai.Client(api_key=gemini_api_key)
            self.use_gemini = True
            print("[OK] Gemini Vision initialized successfully")
        except Exception as e:
            print(f"[WARNING] Gemini Vision initialization failed: {e}")
            print("  Falling back to Google Vision only")
            self.use_gemini = False
            self.gemini_client = None

    
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
        print("\n[1/3] Checking for exposed wires...")
        criterion1 = self.check_exposed_wires({
            "ceiling": image_paths["ceiling"],
            "wall": image_paths["wall"],
            "floor": image_paths["floor_general"]
        })
        results["criteria"].append(criterion1)
        
        # Criterion 2: Floor Joints (1 image)
        print("\n[2/3] Checking floor joints...")
        criterion2 = self.check_floor_joints(image_paths["floor_prep"])
        results["criteria"].append(criterion2)
        
        # Criterion 3: Lighting Adequacy (1 image)
        print("\n[3/3] Checking lighting...")
        criterion3 = self.check_lighting(image_paths["lighting"])
        results["criteria"].append(criterion3)
        
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
            
            print(f"[OK] Image analyzed successfully")
            
            return {
                "objects": [(obj.name, obj.score) for obj in response.localized_object_annotations],
                "labels": [(label.description, label.score) for label in response.label_annotations],
                "properties": response.image_properties_annotation
            }
        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            return {"objects": [], "labels": [], "properties": None}
    
    def _detect_with_gemini(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """Detect using Gemini Vision with custom prompt"""
        if not self.use_gemini or not self.gemini_client:
            return None
        
        try:
            print(f"[INFO] Using Gemini Vision for analysis...")
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Create image part
            import base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Generate content with the image inline
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',  # Updated to compatible model for v1beta
                contents=[
                    prompt,
                    {
                        'inline_data': {
                            'mime_type': 'image/jpeg',
                            'data': image_b64
                        }
                    }
                ]
            )
            
            print(f"[OK] Gemini analysis complete")
            
            # Try to parse as JSON
            try:
                result_text = response.text.strip()
                # Remove markdown code blocks if present
                if result_text.startswith('```'):
                    result_text = result_text.split('```')[1]
                    if result_text.startswith('json'):
                        result_text = result_text[4:]
                result = json.loads(result_text.strip())
                return result
            except:
                # If not JSON, return as text
                return {"raw_response": response.text}
                
        except Exception as e:
            print(f"[WARNING] Gemini Vision error: {e}")
            print(f"  Falling back to Google Vision")
            return None



    
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
        """Check for AC units on facade using Gemini Vision (with Google Vision fallback)"""
        results = {
            "criterion_id": 2,
            "criterion_name": "وحدات التكييف على الواجهة",
            "criterion_name_en": "AC Units on Facade",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {},
            "ai_used": "gemini"  # Track which AI was used
        }
        
        # Try Gemini Vision first
        gemini_result = None
        if self.use_gemini:
            prompt = """قم بتحليل هذه الصورة للواجهة الخارجية بعناية:

المهمة: الكشف عن وحدات التكييف الخارجية (Split AC Units, HVAC Outdoor Units, Air Conditioner Condensers)

ابحث عن:
- وحدات التكييف المثبتة على الجدار الخارجي
- الوحدات الخارجية للمكيفات
- أجهزة الضغط (Compressors)
- المكثفات (Condensers)

أجب بصيغة JSON فقط:
{
  "has_ac_units": true أو false,
  "count": عدد الوحدات (رقم),
  "confidence": نسبة الثقة من 0 إلى 100,
  "description": "وصف مختصر بالعربية"
}"""
            
            gemini_result = self._detect_with_gemini(image_path, prompt)
        
        # Use Gemini results if available
        if gemini_result and isinstance(gemini_result, dict) and "has_ac_units" in gemini_result:
            print(f"[OK] Using Gemini Vision results")
            has_ac = gemini_result.get("has_ac_units", False)
            ac_count = gemini_result.get("count", 0)
            confidence = gemini_result.get("confidence", 90) / 100  # Convert to 0-1 scale
            description = gemini_result.get("description", "تم التحليل بواسطة Gemini")
            
            results["details"]["facade"] = {
                "has_ac_units": has_ac,
                "unit_count": ac_count,
                "confidence": float(confidence),
                "description": description,
                "detected_units": [f"AC Unit {i+1}" for i in range(ac_count)]
            }
            
            if ac_count > 0:
                results["status"] = "non_compliant"
                results["score"] = max(30, 98 - (ac_count * 10))  # Decrease score based on count
            else:
                results["status"] = "compliant"
                results["score"] = 98
            
            results["confidence"] = float(confidence)
            results["ai_used"] = "gemini"
            
        else:
            # Fallback to Google Vision
            print(f"[WARNING] Falling back to Google Vision for AC detection")
            results["ai_used"] = "google_vision"
            
            detection = self._detect_objects_in_image(image_path)
            
            # Debug: Print all detected objects and labels
            print(f"DEBUG - Detected objects: {[obj for obj, _ in detection['objects']]}")
            print(f"DEBUG - Detected labels: {[label for label, _ in detection['labels']]}")
            
            # Check for AC unit related objects - EXPANDED KEYWORDS
            ac_keywords = [
                'air conditioner', 'ac unit', 'hvac', 'cooling unit', 'condenser',
                'air conditioning', 'machine', 'unit', 'cooling', 'compressor',
                'split', 'outdoor unit', 'aircon', 'climate control', 'fan'
            ]
            found_ac_units = []
            
            for obj_name, score in detection["objects"]:
                if any(keyword in obj_name.lower() for keyword in ac_keywords):
                    found_ac_units.append((obj_name, score))
                    print(f"DEBUG - Found AC in objects: {obj_name} (score: {score})")
            
            for label, score in detection["labels"]:
                if any(keyword in label.lower() for keyword in ac_keywords):
                    if label not in [f[0] for f in found_ac_units]:
                        found_ac_units.append((label, score))
                        print(f"DEBUG - Found AC in labels: {label} (score: {score})")
            
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
        """Check for floor joints/cracks using Gemini Vision AI"""
        results = {
            "criterion_id": 3,
            "criterion_name": "الأرضيات بدون فواصل",
            "criterion_name_en": "Seamless Flooring",
            "status": "compliant",
            "score": 0,
            "confidence": 0,
            "details": {}
        }
        
        # Try Gemini Vision first for intelligent analysis
        prompt = """Analyze this restaurant floor image with EXTREME STRICTNESS for hygiene compliance.

Return your analysis in this EXACT JSON format:
{
  "floor_type": "ceramic/marble/epoxy/vinyl/porcelain/other",
  "has_visible_joints": true/false,
  "has_tile_pattern": true/false,
  "joint_severity": "none/minor/moderate/severe",
  "description_ar": "وصف تفصيلي بالعربية عن حالة الأرضية",
  "description_en": "Detailed description in English about floor condition",
  "compliance_status": "compliant/needs_improvement/non_compliant",
  "confidence": 0.95
}

CRITICAL DETECTION POINTS:
1. **Tile Patterns**: ANY visible square, rectangular, or geometric tile pattern = NON-COMPLIANT
2. **Grout Lines**: ANY visible lines between tiles (even faint) = NON-COMPLIANT  
3. **Ceramic/Porcelain Tiles**: Traditional tiled floors with grout = ALWAYS NON-COMPLIANT
4. **Texture Variation**: Regular patterns suggesting individual tiles = NON-COMPLIANT

COMPLIANT ONLY IF:
- Completely seamless surface (epoxy, polished concrete, resin)
- NO visible lines, joints, or grout whatsoever
- Uniform surface with no tile pattern visible
- Appears as one continuous surface

BE ULTRA-STRICT: Restaurant hygiene standards require ZERO visible joints or tile patterns.
If you see ANY indication of tiles or grout lines, mark as "non_compliant" even if minor."""

        gemini_result = self._detect_with_gemini(image_path, prompt)
        
        if gemini_result and isinstance(gemini_result, dict) and "has_visible_joints" in gemini_result:
            # Successfully got structured response from Gemini
            print("[OK] Using Gemini Vision result for floor analysis")
            
            confidence = gemini_result.get("confidence", 0.90)
            has_joints = gemini_result.get("has_visible_joints", False)
            has_tile_pattern = gemini_result.get("has_tile_pattern", False)
            severity = gemini_result.get("joint_severity", "none")
            status = gemini_result.get("compliance_status", "compliant")
            
            results["details"]["floor"] = {
                "floor_type": gemini_result.get("floor_type", "unknown"),
                "has_joints": has_joints,
                "has_tile_pattern": has_tile_pattern,
                "severity": severity,
                "confidence": float(confidence),
                "description": gemini_result.get("description_ar", "تحليل الأرضية"),
                "description_en": gemini_result.get("description_en", "Floor analysis"),
                "analysis_method": "gemini_vision"
            }
            
            # Map status from Gemini response - BE EXTRA STRICT
            # ANY tile pattern or joints = non-compliant
            if status == "non_compliant" or severity == "severe" or has_tile_pattern:
                results["status"] = "non_compliant"
                results["score"] = 40
            elif status == "needs_improvement" or severity == "moderate":
                results["status"] = "needs_improvement"
                results["score"] = 70
            else:
                results["status"] = "compliant"
                results["score"] = 95
            
            results["confidence"] = float(confidence)
            
        else:
            # Fallback to Google Vision if Gemini fails
            print("[WARNING] Gemini failed, falling back to Google Vision for floor analysis")
            
            detection = self._detect_objects_in_image(image_path)
            
            # ULTRA-STRICT: Expanded keywords to catch ANY tile indication
            tile_keywords = [
                # Direct tile/grout indicators
                'tile', 'tiles', 'tiled', 'ceramic', 'porcelain', 'grout', 'grouted',
                # Joint/seam indicators
                'joint', 'joints', 'seam', 'seams', 'gap', 'gaps', 'crack', 'cracks',
                'grout line', 'grout lines', 'tile pattern', 'tiling',
                # Floor type indicators (usually tiled)
                'floor tile', 'ceramic floor', 'tiled floor', 'bathroom tile',
                'kitchen tile', 'flooring', 'tile flooring',
                # Pattern indicators
                'pattern', 'grid', 'square', 'rectangular', 'geometric'
            ]
            
            found_tile_indicators = []
            
            # Check both objects and labels
            for obj_name, score in detection["objects"]:
                obj_lower = obj_name.lower()
                if any(keyword in obj_lower for keyword in tile_keywords):
                    found_tile_indicators.append((obj_name, score, "object"))
                    print(f"[TILE DETECTED] Object: {obj_name} (score: {score})")
            
            for label, score in detection["labels"]:
                label_lower = label.lower()
                if any(keyword in label_lower for keyword in tile_keywords):
                    if label not in [f[0] for f in found_tile_indicators]:
                        found_tile_indicators.append((label, score, "label"))
                        print(f"[TILE DETECTED] Label: {label} (score: {score})")
            
            tile_count = len(found_tile_indicators)
            confidence = 0.80  # Higher confidence for improved fallback
            
            # BE ULTRA-STRICT: ANY tile indication = non-compliant
            has_tiles = tile_count > 0
            
            results["details"]["floor"] = {
                "has_joints": has_tiles,
                "has_tile_pattern": has_tiles,
                "tile_indicator_count": tile_count,
                "confidence": float(confidence),
                "description": f"تم اكتشاف {tile_count} مؤشر للبلاط - غير مستوفي" if has_tiles else "لا توجد مؤشرات للبلاط - الأرضية قد تكون موحدة",
                "detected_indicators": [f"{name} ({source})" for name, _, source in found_tile_indicators],
                "analysis_method": "google_vision_fallback_strict"
            }
            
            
            # ULTRA-STRICT LOGIC: ANY tile indication = immediate fail
            if tile_count >= 1:  # ANY tile indicator = non-compliant
                results["status"] = "non_compliant"
                results["score"] = 30
            else:  # 0 indicators = seamless floor
                results["status"] = "compliant"
                results["score"] = 85  # Lower score for fallback uncertainty
            
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
