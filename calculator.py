import wx

class Calculator(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Calculator, self).__init__(*args, **kwargs)
        
        # Create a panel to hold the buttons and display
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Create a display area (TextCtrl) for showing input and results
        self.display = wx.TextCtrl(panel, style=wx.TE_RIGHT)
        vbox.Add(self.display, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=28)
        
        # Create a grid sizer with 4 rows and 4 columns for the calculator buttons
        grid = wx.GridSizer(4, 4, 5, 5)

        # Add buttons (numbers, operators, clear, equals)
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]
        
        # Loop to create buttons and add them to the grid
        for label in buttons:
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, self.on_button_click)
            grid.Add(button, 0, wx.EXPAND)
        
        # Add the grid of buttons to the vertical box layout
        vbox.Add(grid, proportion=1, flag=wx.EXPAND)
        
        # Set the sizer for the panel
        panel.SetSizer(vbox)
        
        # Frame properties
        self.SetSize((300, 400))
        self.SetTitle("Calculator")
        self.Center()
        
        # Initialize an empty expression string
        self.current_expression = ""

    # Method to handle button clicks
    def on_button_click(self, event):
        # Get the label of the button that was clicked
        button = event.GetEventObject()
        label = button.GetLabel()
        
        # If 'C' is pressed, clear the expression and display
        if label == 'C':
            self.current_expression = ""
            self.display.Clear()
        
        # If '=' is pressed, evaluate the expression and show the result
        elif label == '=':
            try:
                # Evaluate the current expression
                result = eval(self.current_expression)
                # Display the result and update the current expression
                self.display.SetValue(str(result))
                self.current_expression = str(result)
            except Exception as e:
                # If there's an error in evaluation, display "Error" and clear the expression
                self.display.SetValue("Error")
                self.current_expression = ""
        
        # For any other button, append the label to the current expression
        else:
            self.current_expression += label
            self.display.SetValue(self.current_expression)

# Application class
class MyApp(wx.App):
    def OnInit(self):
        frame = Calculator(None)
        frame.Show()
        return True

# Main loop
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
