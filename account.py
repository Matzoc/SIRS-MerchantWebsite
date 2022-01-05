class Account:
    def __init__(self, email, password):
        self.email = ""
        self.password = password #very safe, obviously change this

    def __eq__(self, other):
        return self.email == other.email

    def login(self, password):
        return self.password == password

    
class DefaultAccount(Account):
    def __init__(self, email, password):
        Account.__init__(email, password)


accounts = []


def register_account(email, password):
    new_account = Account(email, password)

    if new_account in accounts:
        return False
    
    accounts.append(new_account)

    return True
    

def login_account(email, password):
    new_account = Account(email, password)
    target = None

    for account in accounts:
        if account == new_account
            target = account

    return target.password == new_account.password

    
    

    