import tkinter as tk
from chromaspeclib.datatypes.command import *
from chromaspeclib.datatypes.types   import *
from chromaspeclib.expert            import ChromaSpecExpertInterface as expert

class Spectrometer(tk.Canvas):
  def __init__(self, *args, **kwargs):
    tk.Canvas.__init__(self, *args, **kwargs)
    self.create_rectangle(50, 50, 100, 100)

  def redraw(self, pixels):
    pass

class BridgeLED(tk.Frame):
  def __init__(self, *args, **kwargs):
    tk.Frame.__init__(self, *args, **kwargs)
    self.state = tk.IntVar()
    self.label = tk.Label(self, text="Bridge LED", justify=tk.LEFT, padx=10)
    self.off   = tk.Radiobutton(self, text="Off",   padx=10, variable=self.state, value=LEDOff,  command=lambda:self.usb_send(self.state.get()))
    self.green = tk.Radiobutton(self, text="Green", padx=10, variable=self.state, value=LEDGreen,command=lambda:self.usb_send(self.state.get()))
    self.red   = tk.Radiobutton(self, text="Red",   padx=10, variable=self.state, value=LEDRed,  command=lambda:self.usb_send(self.state.get()))
    self.label.grid(row=0, column=0)
    self.off.grid(  row=0, column=1)
    self.green.grid(row=0, column=2)
    self.red.grid(  row=0, column=3)

  def usb_send(self, state):
    self.master.push_command(CommandSetBridgeLED(led_num=0, led_setting=state), self)

  def usb_receive(self, reply):
    if reply and reply.status == 0 and hasattr(reply, "led_setting"):
      self.set(reply.led_setting)

  def set(self, state):
    self.state.set(state)

  def get(self):
    return self.state.get()
  
class ChromaspecGUI(tk.Frame):
  def __init__(self, *args, **kwargs):
    tk.Frame.__init__(self, *args, **kwargs)
    self.spec = Spectrometer(self, width=400, height=600)
    self.led  = BridgeLED(self)

    self.spec.grid(row=0, column=0)
    self.led.grid( row=0, column=1)

    self.queue = []
    self.wait  = []

    self.usb  = expert() #emulation=True)

    self.push_command(CommandGetBridgeLED(led_num=0), self.led)
    #led = self.usb.getBridgeLED(led_num=0)
    #if led:
    #  self.led.set(led.led_setting)

    self.main_thread()

  def push_command(self, command, requestor):
    self.queue.append((command, requestor))

  def usb_receive(self, reply):
    if reply and reply.status == 0:
      #print("pixels: %s"%(reply))
      pass

  def main_thread(self):
    self.push_command(CommandCaptureFrame(), self)

    reply = self.usb.receiveReply()
    while reply:
      recipient = self.wait.pop(0)
      recipient[1].usb_receive(reply)
      reply = self.usb.receiveReply()

    while self.queue:
      command = self.queue.pop(0)
      self.usb.sendCommand(command[0])
      self.wait.append(command)

    #pixels = self.usb.captureFrame()
    #print(pixels)
    #led = self.usb.getBridgeLED(led_num=0)
    #if led:
    #  self.led.set(led.led_setting)

    self.after(100, self.main_thread)
    
    
    

root = tk.Tk()
gui = ChromaspecGUI(root)
gui.pack()
gui.mainloop()
