from datetime import datetime, timedelta


class Ledger:
    def __init__(self):
        self.wallets = []
        self.handout_amount = 500

    def _load_ledger(self):
        self.wallets = []
        with open("assets/balances.txt", "r") as f:
            unformatted_wallets = [x.strip().split(" ") for x in f.readlines()]

            for x in unformatted_wallets:
                if len(x) == 2:
                    print("Updating balances to new format")
                    x.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    x[2] = " ".join(x[2:4])
                    del x[3]

            self.wallets = [Wallet(x[0], int(x[1]), datetime.strptime(
                x[2], "%Y-%m-%d %H:%M:%S")) for x in unformatted_wallets]

    def _save_ledger(self):
        with open("assets/balances.txt", "w") as f:
            for wallet in self.wallets:
                f.write(f"{wallet.authorid} {wallet.balance} {
                        wallet.lasthandout.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def find_wallet_by_authorid(self, id):
        self._load_ledger()
        for wallet in self.wallets:
            if wallet.authorid == id:
                return wallet
        return None

    def update_balance_by_authorid(self, id, amount):
        self._load_ledger()
        wallet = self.find_wallet_by_authorid(id)
        if wallet:
            wallet.balance += amount
            wallet.lasthandout = datetime.now()
        self._save_ledger()

    def handout(self, id):
        self.update_balance_by_authorid(id, self.handout_amount)

    def is_handout_valid(self, id):
        self._load_ledger()
        wallet = self.find_wallet_by_authorid(id)
        if wallet:
            return datetime.now() - wallet.lasthandout >= timedelta(days=1)
        return False

    def is_bet_high(self, id, bet):
        self._load_ledger()
        wallet = self.find_wallet_by_authorid(id)
        if wallet.balance < bet:
            return True
        return False


class Wallet:
    def __init__(self, authorid, balance, lasthandout):
        self.authorid = authorid
        self.balance = balance
        self.lasthandout = lasthandout
