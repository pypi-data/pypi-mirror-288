import json
import ao

class Orderbook:
    def __init__(self, signer, orderbook_process, settle_process):
        self.signer = signer
        self.ob_process = orderbook_process
        self.st_process = settle_process
    
    def deposit(self, token_process, amount):
        m, r = ao.send_and_get(self.signer, token_process, '', {
            'Action': 'Transfer', 
            'Recipient': self.ob_process,
            'Quantity': str(amount)
        })
        return m, r
    
    def withdraw(self, token_process, amount):
        m, r = ao.send_and_get(self.signer, self.ob_process, '', {
            'Action': 'Withdraw', 
            'AssetID': token_process,
            'Quantity': str(amount)
        })
        return m, r
    
    def balances(self):
        r = ao.dry_run(self.signer, self.ob_process, '', {
            'Action': 'Balances'
        })
        return json.loads(r['Messages'][0]['Data'])
    
    def make_order(self, token_in, token_out, amount_in, amount_out):
        m, r = ao.send_and_get(self.signer, self.ob_process, '', {
            'Action': 'MakeOrder', 
            'AssetID': token_in, 
            'Amount': str(amount_in),
            'HolderAssetID': token_out,
            'HolderAmount': str(amount_out),
        })
        return m, r
    
    def get_orders(self, token_in, token_out, status='open', desc=True, page=1, page_size=10):
        if desc:
            order = 'desc'
        else:
            order = 'asc'
        r = ao.dry_run(self.signer, self.st_process,  '', {
            'Action': 'GetNotes', 
            'AssetID': token_in, 
            'HolderAssetID': token_out,
            'Order': order, # order by price
            'Status': status, #  'Status': 'open, canceled, settled'
            'Page': str(page),
            'PageSize': str(page_size)
        })
        return json.loads(r['Messages'][0]['Data'])
    
    def get_order(self, note_id):
        r = ao.dry_run(self.signer, self.st_process,  '', {
            'Action': 'GetNote', 
            'NoteID': note_id, 
        })
        return json.loads(r['Messages'][0]['Data'])
    
    def get_my_orders(self, token_in, token_out, status='open', desc=True, page=1, page_size=10):
        if desc:
            order = 'desc'
        else:
            order = 'asc'
        r = ao.dry_run(self.signer, self.ob_process,  '', {
            'Action': 'GetOrders', 
            'AssetID': token_in, 
            'HolderAssetID': token_out,
            'Order': order, # order issue date
            'Status': status, #  'Status': 'open, canceled, settled'
            'Page': str(page),
            'PageSize': str(page_size)
        })
        return json.loads(r['Messages'][0]['Data'])
    
    def cancel_order(self, note_id):
        m, r = ao.send_and_get(self.signer, self.ob_process, '', {
            'Action': 'CancelOrder', 
            'NoteID': note_id
        })
        return m, r

    def take_order(self, order):
        m, r = ao.send_and_get(self.signer, self.ob_process, '', {
            'Action': 'TakeOrder', 
           }, 
           data=json.dumps(order)
        )
        return m, r