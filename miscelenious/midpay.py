import json
import os
import time
from datetime import datetime

class MidPay:
    def __init__(self):
        self.transactions = {}
        self.escrow_account = 0
        self.setup_bank_files()
        
    def setup_bank_files(self):
        """Initialize bank account files if they don't exist"""
        # Create A's bank account if it doesn't exist
        if not os.path.exists("A_bank.json"):
            with open("A_bank.json", "w") as f:
                json.dump({"balance": 1000, "transactions": []}, f, indent=4)
        
        # Create B's bank account if it doesn't exist
        if not os.path.exists("B_bank.json"):
            with open("B_bank.json", "w") as f:
                json.dump({"balance": 500, "transactions": []}, f, indent=4)
    
    def get_balance(self, user):
        """Get the balance of a user's account"""
        with open(f"{user}_bank.json", "r") as f:
            data = json.load(f)
        return data["balance"]
        
    def create_transaction(self, amount, service_description):
        """A initiates a payment to MidPay"""
        # Check if A has sufficient balance
        a_balance = self.get_balance("A")
        if a_balance < amount:
            return {"status": "failed", "message": "Insufficient funds in A's account"}
        
        # Generate transaction ID
        transaction_id = str(int(time.time()))
        
        # Store transaction details
        self.transactions[transaction_id] = {
            "amount": amount,
            "service": service_description,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None,
            "released_at": None
        }
        
        # Deduct from A's account and move to escrow
        self._update_balance("A", -amount, f"Payment to escrow for {service_description} [ID: {transaction_id}]")
        self.escrow_account += amount
        
        return {
            "status": "success", 
            "message": f"Payment of ${amount} moved to escrow. Transaction ID: {transaction_id}",
            "transaction_id": transaction_id
        }
    
    def mark_service_completed(self, transaction_id):
        """B marks the service as completed"""
        if transaction_id not in self.transactions:
            return {"status": "failed", "message": "Invalid transaction ID"}
        
        if self.transactions[transaction_id]["status"] != "pending":
            return {"status": "failed", "message": "Transaction is not in pending state"}
        
        # Mark service as completed
        self.transactions[transaction_id]["status"] = "completed"
        self.transactions[transaction_id]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "status": "success", 
            "message": "Service marked as completed. Waiting for confirmation from A."
        }
    
    def confirm_completion(self, transaction_id):
        """A confirms that the service has been completed, releasing funds to B"""
        if transaction_id not in self.transactions:
            return {"status": "failed", "message": "Invalid transaction ID"}
        
        if self.transactions[transaction_id]["status"] != "completed":
            return {"status": "failed", "message": "Service not yet marked as completed by B"}
        
        # Release funds to B
        amount = self.transactions[transaction_id]["amount"]
        service = self.transactions[transaction_id]["service"]
        
        self._update_balance("B", amount, f"Payment received for {service} [ID: {transaction_id}]")
        self.escrow_account -= amount
        
        # Update transaction status
        self.transactions[transaction_id]["status"] = "released"
        self.transactions[transaction_id]["released_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "status": "success", 
            "message": f"Payment of ${amount} released to B."
        }
    
    def cancel_transaction(self, transaction_id):
        """A cancels the transaction, returning funds from escrow"""
        if transaction_id not in self.transactions:
            return {"status": "failed", "message": "Invalid transaction ID"}
        
        if self.transactions[transaction_id]["status"] == "released":
            return {"status": "failed", "message": "Cannot cancel - funds already released"}
        
        # Return funds to A
        amount = self.transactions[transaction_id]["amount"]
        service = self.transactions[transaction_id]["service"]
        
        self._update_balance("A", amount, f"Refund for cancelled service: {service} [ID: {transaction_id}]")
        self.escrow_account -= amount
        
        # Update transaction status
        self.transactions[transaction_id]["status"] = "cancelled"
        
        return {
            "status": "success", 
            "message": f"Transaction cancelled. ${amount} returned to A."
        }
    
    def _update_balance(self, user, amount, description):
        """Update a user's balance and record the transaction"""
        with open(f"{user}_bank.json", "r") as f:
            data = json.load(f)
        
        data["balance"] += amount
        data["transactions"].append({
            "amount": amount,
            "description": description,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        with open(f"{user}_bank.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def get_transaction_status(self, transaction_id):
        """Get the status of a transaction"""
        if transaction_id not in self.transactions:
            return {"status": "failed", "message": "Invalid transaction ID"}
        
        return {
            "status": "success",
            "transaction": self.transactions[transaction_id]
        }
    
    def display_accounts(self):
        """Display current balances and escrow amount"""
        a_balance = self.get_balance("A")
        b_balance = self.get_balance("B")
        
        print("\n=== ACCOUNT SUMMARY ===")
        print(f"A's Balance: ${a_balance}")
        print(f"B's Balance: ${b_balance}")
        print(f"Escrow: ${self.escrow_account}")
        print("=======================\n")


def run_simulation():
    midpay = MidPay()
    print("\nWelcome to MidPay Simulation!")
    
    while True:
        print("\n=== MENU ===")
        print("1. View Account Balances")
        print("2. Create New Transaction (as A)")
        print("3. Mark Service as Completed (as B)")
        print("4. Confirm and Release Payment (as A)")
        print("5. Cancel Transaction (as A)")
        print("6. Check Transaction Status")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            midpay.display_accounts()
            
        elif choice == "2":
            amount = float(input("Enter amount to pay: $"))
            description = input("Enter service description: ")
            result = midpay.create_transaction(amount, description)
            print(f"\nResult: {result['message']}")
            
        elif choice == "3":
            trans_id = input("Enter transaction ID: ")
            result = midpay.mark_service_completed(trans_id)
            print(f"\nResult: {result['message']}")
            
        elif choice == "4":
            trans_id = input("Enter transaction ID: ")
            result = midpay.confirm_completion(trans_id)
            print(f"\nResult: {result['message']}")
            
        elif choice == "5":
            trans_id = input("Enter transaction ID: ")
            result = midpay.cancel_transaction(trans_id)
            print(f"\nResult: {result['message']}")
            
        elif choice == "6":
            trans_id = input("Enter transaction ID: ")
            result = midpay.get_transaction_status(trans_id)
            if result["status"] == "success":
                print("\nTransaction Details:")
                print(json.dumps(result["transaction"], indent=4))
            else:
                print(f"\nError: {result['message']}")
            
        elif choice == "7":
            print("\nThank you for using MidPay!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    run_simulation()