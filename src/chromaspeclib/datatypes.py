class ChromationStatus:
  def __init__( self, message=None ):
    if message:
      self.message = str(message)
  def __str__( self ):
    return self.message

class ChromationStatusOK(ChromationStatus):
  def __init__( self, message="OK" ):
    ChromationStatus.__init__( self, message )
    
class ChromationStatusError(ChromationStatus):
  def __init__( self, message="Error" ):
    ChromationStatus.__init__( self, message )
    

