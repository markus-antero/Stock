error handling
--------------
try:
    # catch exc if index out of range
    print 'Looks like a bad index'

except:
    # catch something we didn't anticipate
    print 'Exception type:', sys.exc_info()[0]
    print 'Exception value:', sys.exc_info()[1]
    traceback.print_exc()    
finally:
    print ('executes always')