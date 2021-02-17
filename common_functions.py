from time import sleep



## Dynamic wait + Raise clean failure if element not found
def waitfor(self, timeout, attribute, value, suppressfailure=1):
    #suppressfailure disable= 1
    #suppressfailure enable = 0
    driver = self.driver
    thinktime = 1
    status = False
    while True:

        try:
            if (driver.find_elements(attribute, value).__len__() > 0):
                status = True
            else:
                status = False
        except:
            status = False

        if (status == True):
            break
        else:
            thinktime = thinktime + 1
            sleep(1)

        if thinktime > timeout:
            if (suppressfailure == 1):
                print("TimeOut: [FAILED] Element " + attribute + " with value " + value + " not found")
                self.fail("Case Status: [Failed]")
            #else:
            #    print("debug: Element " + attribute + " with value " + value + " not found")
            break
    return status

def logit(msg,log_level=0):
    ### We can create a more advanced logger function to analyze and process logs. - Not in the scope of this interview
    if log_level == 0:  #Verbose
        print(msg)
    #Verbose
    #Debug
    #Production
    #Error
    #Exceptions
    #Libissues
    ## So many possibilities here :)
