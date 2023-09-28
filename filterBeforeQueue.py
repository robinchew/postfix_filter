import purepythonmilter as ppm

async def on_mail_from(cmd: ppm.MailFrom) -> ppm.VerdictOrContinue:

    if isSpam(cmd):
        return ppm.RejectWithCode(primary_code=(3, 3, 3), text="Not Allowed")
    else:
        return ppm.Continue()

def isSpam(cmd):

    if cmd.address.lower().endswith("example.com"):
        return True
    
    return False


if __name__=='__main__':
    milterPy = ppm.PurePythonMilter(name="mymilter", hook_on_mail_from=on_mail_from)
    milterPy.run_server(host="127.0.0.1", port=9000)