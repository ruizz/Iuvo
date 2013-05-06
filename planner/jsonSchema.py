jsonSchema = {
    "name": {"type": "string"},
    "courseGroups": {
        "type": "array",
        "items": {
            "name": {"type": "string"},
            "columnNumber": {"type": "integer"},
            "courseSlots": {
                "type": "array", 
                "items": {   
                    "dept": {"type": "string"},
                    "number": {"type": "integer"},
                    "hours": {"type": "integer"},
                    "isDepartmentEditable": {"type": "boolean"},
                    "isNumberEditable": {"type": "boolean"} 
                }
            }
        }
    }
}