import os
class SetupUtils:
    # Install local wheel file
    @staticmethod
    def GetWheelFile(name: str,file_path: str) -> str:
        """Returns a path to a local package."""
        file_path=os.path.join(os.getcwd(),"wheels",file_path)
        return f"{name} @ file://{file_path}"

    # Merge two lists and remove duplicates
    @staticmethod
    def MergeList(list1, list2):
        # Ensure both list1 and list2 are lists, default to empty list if None
        list1 = list1 if list1 is not None else []
        list2 = list2 if list2 is not None else []
        return list(set(list1) | set(list2))
    
    @staticmethod
    def ParseRequirements(filepath):
        required=[]
        if os.path.exists(filepath):
            with open(filepath) as f:
                required = f.read().splitlines()
            return required
        raise Exception(f"File not found: {filepath}")