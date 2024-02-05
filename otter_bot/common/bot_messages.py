class Messages:
    """Dependency to inject messages"""

    @staticmethod
    def advanced_process_message(user: str, company: str, process_state: str) -> str:
        """Message when there is an advanced process"""
        return f"{user} has an advanced process with {company}, can't have {process_state} at this point. ❌"
    

    @staticmethod
    def final_desicion_message(user: str, company: str) -> str:
        """Message when a final desicion has been made previously in the process"""
        return f"{user} has already received a desicion from {company}. ❌"
    

    @staticmethod
    def successful_insertion_message(user: str, company: str, from_offer: bool, from_rejection: bool, process_state: str) -> str:
        """Message when the insertion has been successful"""
        if from_offer:
            return f"{user} has received {process_state} from {company}. 🎉"
        elif from_rejection:
            return f"{user} has received {process_state} from {company}. 😭"
        else:
            return f"{user} has received {process_state} from {company}. ✅"
    

    @staticmethod
    def apply_message(user: str, company: str) -> str:
        """Message when the user has applied successfuly"""
        return f"{user} has applied to {company} successfuly. ✅"
    

    @staticmethod
    def proper_procedure_message(user: str, company: str) -> str:
        """Message when the user is not using the commands properly"""
        return f"{user} must apply to {company} before trying to use this command. ❌"