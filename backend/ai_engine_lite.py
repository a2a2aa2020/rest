"""
Lightweight AI Engine for Restaurant Inspection (Mock Version)
Works without OpenCV - perfect for Render Free Tier
"""
import random
from typing import Dict, Any
from PIL import Image
import io


class InspectionAIEngine:
    """Lightweight AI Engine using mock analysis"""
    
    def __init__(self):
        """Initialize AI engine"""
        print("Lightweight AI Engine initialized")
    
    def analyze_inspection(self, image_paths: Dict[str, str]) -> Dict[str, Any]:
        """
        Main analysis function - Mock version
        Returns realistic results without heavy processing
        """
        # Generate realistic scores
        criterion1_score = random.randint(85, 98)
        criterion2_score = random.randint(88, 99)
        criterion3_score = random.randint(75, 95)
        criterion4_score = random.randint(80, 96)
        
        results = {
            "overall_status": "compliant",
            "overall_score": 0,
            "criteria": []
        }
        
        # Criterion 1: Exposed Wires/Cables
        results["criteria"].append({
            "criterion_id": 1,
            "criterion_name": "الأسلاك والأنابيب الظاهرة",
            "criterion_name_en": "Exposed Wires and Pipes",
            "status": "compliant" if criterion1_score >= 80 else "non_compliant",
            "score": criterion1_score,
            "confidence": random.uniform(0.85, 0.95),
            "details": {
                "ceiling": {"has_exposed_wires": False, "confidence": 0.92, "description": "لا توجد أسلاك ظاهرة في السقف"},
                "wall": {"has_exposed_wires": False, "confidence": 0.89, "description": "لا توجد أسلاك ظاهرة في الجدران"},
                "floor": {"has_exposed_wires": False, "confidence": 0.91, "description": "لا توجد أنابيب ظاهرة"}
            },
            "images_analyzed": 3
        })
        
        # Criterion 2: AC Units
        results["criteria"].append({
            "criterion_id": 2,
            "criterion_name": "وحدات التكييف على الواجهة",
            "criterion_name_en": "AC Units on Facade",
            "status": "compliant" if criterion2_score >= 80 else "non_compliant",
            "score": criterion2_score,
            "confidence": random.uniform(0.88, 0.96),
            "details": {
                "facade": {
                    "has_ac_units": False,
                    "unit_count": 0,
                    "confidence": 0.93,
                    "description": "لا توجد وحدات تكييف ظاهرة على الواجهة"
                }
            }
        })
        
        # Criterion 3: Floor Joints
        results["criteria"].append({
            "criterion_id": 3,
            "criterion_name": "الأرضيات بدون فواصل",
            "criterion_name_en": "Seamless Flooring",
            "status": "compliant" if criterion3_score >= 70 else "needs_improvement",
            "score": criterion3_score,
            "confidence": random.uniform(0.80, 0.92),
            "details": {
                "floor": {
                    "has_joints": criterion3_score < 85,
                    "joint_count": 0 if criterion3_score >= 85 else random.randint(2, 5),
                    "confidence": 0.87,
                    "description": "الأرضية موحدة" if criterion3_score >= 85 else "بعض الفواصل البسيطة"
                }
            }
        })
        
        # Criterion 4: Lighting
        results["criteria"].append({
            "criterion_id": 4,
            "criterion_name": "كفاية الإضاءة",
            "criterion_name_en": "Lighting Adequacy",
            "status": "compliant" if criterion4_score >= 75 else "non_compliant",
            "score": criterion4_score,
            "confidence": random.uniform(0.85, 0.93),
            "details": {
                "lighting": {
                    "brightness_level": random.uniform(140, 180),
                    "is_adequate": True,
                    "confidence": 0.89,
                    "description": "مستوى الإضاءة جيد (75%)"
                }
            }
        })
        
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
        
        return results
