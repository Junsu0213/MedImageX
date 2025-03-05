def get_user_input(prompt, default=None):
    """사용자 입력을 받는 함수"""
    if default:
        user_input = input(f"{prompt} [{default}]: ")
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ") 