####################################################################################################
# Author: Zand Bakhtiari w/help from Brian Kingery
# Date: September 12, 2017
# 
# Credit: Brian Kingary Virginia Department of Transportation
#
# Purpose: To automate Reconcile & Post, compress the SDE database, & Email 
#          GIS staff whether or not there are Conflict were detected.
###################################################################################################
# Import modules
# Acrpy is used for all Geoprocessing > os is used for Creating/Reading/Updating of textfile
# > time is used for the nameing of the output Log.
import arcpy, os
arcpy.env.overwriteOutput = True
                  
#%%
# Email Function 
def Email(RESULTS):
    try:
        import smtplib
        mailServer      = # Email server
        mailRecipients  = [''] # List of email reciptients  EXAMPLE:['Zand Bakhtiari <zbakhtiari@something.something>', 'Mary Jean <mjean@something.something']
        mailSender = '%s <%s #s@omthing.somthing>' % (os.environ['USERNAME'], os.environ['USERNAME'])

        subject = RESULTS + ' while running the Rec and Post Script. Nightly Database Compression Completed.'
        
        body  = '\n' + RESULTS + ' while running the Rec and Post Script.  The nightly database compression was also completed.\n'

        
        body += '\n*****************************************************************\n'
        body += '\nThis is an automatically generated message.  Please do not reply.\n'
        body += '\n*****************************************************************\n'
        

        message  = ''
        message += 'From: %s\r\n' % mailSender
        message += 'To: %s\r\n' % ', '.join(mailRecipients)
        message += 'Subject: %s\r\n\r\n' % subject
        message += '%s\r\n' % body
        server = smtplib.SMTP(mailServer)
        server.sendmail(mailSender, mailRecipients, message)
        server.quit()
    except:
        pass
                            
#%%

# Disconnect All Users

arcpy.DisconnectUser(r'', 'ALL') #The input SDE Connection should go after r

#%%
# Rec and Posts all versions to DEFAULT
#Fill in Edit versions
arcpy.ReconcileVersions_management(input_database= #INPUT SDE, reconcile_mode="ALL_VERSIONS", target_version="sde.DEFAULT", edit_versions= #VERSIONS TO BE RECONCILED, acquire_locks="LOCK_ACQUIRED", abort_if_conflicts="ABORT_CONFLICTS", conflict_definition="BY_OBJECT", conflict_resolution="FAVOR_TARGET_VERSION", with_post="POST", with_delete="KEEP_VERSION", out_log= # OUTPUT FILEPATH OF AND NAME OF .TXT doc)

#%%
# Compress the Database

arcpy.Compress_management(in_workspace= r"") #Input sde Conneciton shoudl go after r

#%%

logpath = r'' # The file path of the output .txt document
x = 0

with open (logpath) as text:
    for line in text:
        if "Warning" in line:
            x+=1
        else:
            pass
if x == 0:
    Email('NO conflicts found')
else:
    Email('Conflicts FOUND')
    
