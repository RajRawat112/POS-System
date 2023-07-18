import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pandas as pd

import Model as Model


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Inventory Management')

        # Create the notebook (tabbed interface)
        notebook = ttk.Notebook(self)
        notebook.pack()

        # Create the Checkout tab
        cart_tab = ttk.Frame(notebook)
        notebook.add(cart_tab, text="Checkout Cart")

        # Create the search and add widgets in the Checkout tab
        label_search = ttk.Label(cart_tab, text='Search Item:')
        label_search.grid(row=0, column=0, sticky=tk.E)
        self.entry_search = ttk.Entry(cart_tab)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        button_search = ttk.Button(cart_tab, text='Search', command=self.search_item)
        button_search.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)

        label_quantity_cart = ttk.Label(cart_tab, text='Quantity:')
        label_quantity_cart.grid(row=1, column=0, sticky=tk.E)
        self.entry_quantity_cart = ttk.Entry(cart_tab)
        self.entry_quantity_cart.grid(row=1, column=1, padx=5, pady=5)

        button_add_to_cart = ttk.Button(cart_tab, text='Add to Cart', command=self.add_to_cart)
        button_add_to_cart.grid(row=1, column=2, padx=5, pady=5, sticky=tk.EW)

        # Create the cart view (Treeview) in the Checkout tab
        self.cart_view = ttk.Treeview(cart_tab, columns=('Item Name', 'Price', 'Quantity'), show='headings')
        self.cart_view.heading('Item Name', text='Item Name')
        self.cart_view.heading('Price', text='Price')
        self.cart_view.heading('Quantity', text='Quantity')
        self.cart_view.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        button_complete_checkout = ttk.Button(cart_tab, text='Complete Checkout', command=self.complete_checkout)
        button_complete_checkout.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Create the Inventory tab
        inventory_tab = ttk.Frame(notebook)
        notebook.add(inventory_tab, text="Inventory")

        # Create the input fields and buttons in the Inventory tab
        label_name = ttk.Label(inventory_tab, text='Item Name:')
        label_name.grid(row=0, column=0, sticky=tk.E)
        self.entry_name = ttk.Entry(inventory_tab)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        label_price = ttk.Label(inventory_tab, text='Item Price:')
        label_price.grid(row=1, column=0, sticky=tk.E)
        self.entry_price = ttk.Entry(inventory_tab)
        self.entry_price.grid(row=1, column=1, padx=5, pady=5)

        label_quantity = ttk.Label(inventory_tab, text='Quantity:')
        label_quantity.grid(row=2, column=0, sticky=tk.E)
        self.entry_quantity = ttk.Entry(inventory_tab)
        self.entry_quantity.grid(row=2, column=1, padx=5, pady=5)

        button_add = ttk.Button(inventory_tab, text='Add Item', command=self.add_item)
        button_add.grid(row=1, column=2, padx=5, pady=5, sticky=tk.EW)

        button_remove = ttk.Button(inventory_tab, text='Remove Item', command=self.remove_item)
        button_remove.grid(row=2, column=2, padx=5, pady=5, sticky=tk.EW)

        # Create the data view (Treeview) in the Inventory tab
        self.data_view = ttk.Treeview(inventory_tab, columns=('Item Name', 'Price', 'Quantity'), show='headings')
        self.data_view.heading('Item Name', text='Item Name')
        self.data_view.heading('Price', text='Price')
        self.data_view.heading('Quantity', text='Quantity')
        self.data_view.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Update the data view initially
        self.update_data_view()

    def add_item(self):
        item_name = self.entry_name.get()
        item_price = self.entry_price.get()
        item_quantity = self.entry_quantity.get()
        Model.add_item(item_name, item_price, item_quantity)
        self.update_data_view()

    def remove_item(self):
        selected_item = self.data_view.focus()
        if selected_item:
            item_name = self.data_view.item(selected_item)['values'][0]
            Model.remove_item(item_name)
            self.update_data_view()

    def update_data_view(self):
        inventory_data = Model.get_inventory_data()
        self.data_view.delete(*self.data_view.get_children())  # Clear the current view
        for item in inventory_data:
            self.data_view.insert('', tk.END, values=(item['Item Name'], item['Price'], item['Quantity']))

    def search_item(self):
        item_name = self.entry_search.get()
        inventory_data = Model.get_inventory_data()
        for item in inventory_data:
            if item['Item Name'] == item_name:
                item_price = item['Price']
                item_quantity = item['Quantity']
                if item_quantity > 0:
                    self.item_price = item_price
                    self.item_quantity = item_quantity
                    self.item_name = item_name
                    self.entry_quantity_cart.delete(0, tk.END)
                    self.entry_quantity_cart.insert(0, '1')
                else:
                    tk.messagebox.showwarning("Out of Stock", "Item is out of stock.")
                break
        else:
            tk.messagebox.showwarning("Item Not Found", "Item not found in the inventory.")

    def add_to_cart(self):
        quantity = int(self.entry_quantity_cart.get())
        if quantity <= self.item_quantity:
            self.cart_view.insert('', tk.END, values=(self.item_name, self.item_price, quantity))
        else:
            tk.messagebox.showwarning("Invalid Quantity", "Quantity exceeds available stock.")

    def complete_checkout(self):
        cart_items = []
        for child in self.cart_view.get_children():
            item_name = self.cart_view.item(child)['values'][0]
            item_price = float(self.cart_view.item(child)['values'][1])
            quantity = int(self.cart_view.item(child)['values'][2])
            cart_items.append({'Item Name': item_name, 'Price': item_price, 'Quantity': quantity})

        # Update inventory quantities
        inventory_data = Model.get_inventory_data()
        for item in cart_items:
            item_name = item['Item Name']
            item_quantity = item['Quantity']
            for inventory_item in inventory_data:
                if inventory_item['Item Name'] == item_name:
                    inventory_item['Quantity'] -= item_quantity
                    break

        # Update inventory Excel file
        inventory_df = pd.DataFrame(inventory_data)
        inventory_df.to_excel(Model.INVENTORY_FILE_PATH, index=False)

        # Print receipts
        total_price = sum(item['Price'] * item['Quantity'] for item in cart_items)
        receipt_text = "Receipt:\n"
        for item in cart_items:
            receipt_text += f"{item['Item Name']}: Price: {item['Price']}, Quantity: {item['Quantity']}\n"
        receipt_text += f"Total Price: {total_price}"
        print(receipt_text)

        # Clear cart view and update inventory view
        self.cart_view.delete(*self.cart_view.get_children())
        self.update_data_view()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
