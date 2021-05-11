import subprocess, json, os, re, pprint, smtplib, ssl
import xml.etree.ElementTree as ET
from JenkinsFileHandler import JenkinsFileHandler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod

class WebHook(ABC):
    """
    Base Abstract class that all modules need to inherit
    This class comes with some utility functions for running CodeCoverage for Dotnet projects
    
    Attributes
    ===========
        keys : dict
            dictionary of credientials
        
    Public Methods 
    ===========
        Run( self, args )
            Abstract class that all classes must implement

        WriteToFile( self, input, fileName )
        CurrentCommitCheck( self )
        CreateCodeCoverage( self, currentDirectoryPath, branchName, mmtResource )
        ReadResults( self, mmtResources, mmtHome, filePath, type )
        SeparateTextFromJson( self, file )
        SendEmail( self, header, textBody, sender, receiver, mime )
    """
    keys = None

    def __init__( self ):
        with open("keys.json", "r") as reader:
            self.keys = json.loads(reader.read())

    @abstractmethod
    def Run( self, args ):
        pass

    @abstractmethod
    def Help( self ):
        pass
    
    def WriteToFile( self, input, fileName ):
        '''
            Write a file from input text

            Parameters
            ============
                input - str 
                    Text to write in file
                fileName - str
                    complete file path and name
        '''
        resultFile = open( fileName,"w" )
        resultFile.write( input )
        resultFile.close(  )
    
    def CurrentCommitCheck( self ):
        '''
        Verify that the current commit is different from CurrentCommit.txt
        '''
        gitTag = subprocess.check_output( [ "git", "rev-parse", "--short", "HEAD" ] )
        
        #If the file does not exist create it
        currentCommit = open( "CurrentCommit.txt", 'a+' )
        
        #If the commits are not equal or its empty then run a full test
        if currentCommit.read( )  != gitTag:
            self.WriteToFile( str(gitTag), "CurrentCommit.txt" )
            currentCommit.close( )
        else:
            currentCommit.close( )
            raise Exception("Commit is the Same")

    def CreateCodeCoverage( self, currentDirectoryPath, branchName, mmtResource ):
        '''
        Create Code coverage from all tests

        Parameters
        =============
            currentDirectoryPath - str
                absolute current working directory
            branchName - str
                git branch to checkout
        '''
        subprocess.call( [ 'git', 'checkout', '-f', str(branchName) ])
        subprocess.call( [ 'git', 'pull'])
        os.chdir('..')
        exitCode = subprocess.call( ['dotnet', 'test', "{0}".format(currentDirectoryPath), '/p:CollectCoverage=true', '/p:CoverletOutputFormat=opencover'] )
        return exitCode


    @classmethod
    def TypeTestResults(self, currentDirectoryPath, type):

        exitCode = subprocess.call( ['dotnet', 'test', currentDirectoryPath, '--logger', 'trx;LogFileName=Results.trx', '--filter', 'Category={0}'.format(type), '/p:CollectCoverage=true', '/p:CoverletOutputFormat=opencover'] )
        return exitCode

    def ReadResults( self, filePath, type ):
        '''
        Gets results from codecoverage and reads XML file

        Parameters
        ==============
            filePath - str
                absolute path to Results.trx
            type - str
                type of tests to run [ all, unit, test, functional ]
        '''
        exitCode = self.TypeTestResults( filePath, type)
        if exitCode:
            tree = ET.parse( filePath )
            root = tree.getroot()
            results = []
            for child in root:
                for c in child:
                    if c.tag[-8:] == "Counters":
                        counterDictionary = c.attrib
            results.append("total: " + counterDictionary['total'] + 
            " passed: " + counterDictionary["passed"] 
            + " failed: " + counterDictionary["failed"])
            print(int(counterDictionary['failed']))
            if int(counterDictionary["failed"]) > 0:
                self.WriteToFile('Failure: Test Failures in New Version of Staging', "Header.txt")
            else:
                self.WriteToFile('Success: New Version of Staging is Available', "Header.txt")

            self.WriteToFile(str(results), "Results.txt")

    def SeparateTextFromJson( self, file ):
        '''
        Extract JSON text from Jenkins log

        Parameters
        =============
            file - str
                path to job file
        '''
        jsonFile = open(file, 'r' )
        readFile = jsonFile.read()

        firstIndex = readFile.index('{')
        lastIndex = readFile.rindex('}\n') + 1
        jsonFile.close()

        return readFile[firstIndex:lastIndex]
    
    def SendEmail( self, header, textBody, sender, receiver, mime ):
        '''
        Send a formatted
        '''
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(sender, self.keys['email_password'])
            message = MIMEMultipart("alternative")
            message["Subject"] = header
            message["From"] = sender
            message["To"] = receiver

            text = """\
                    """ + textBody + """\
                    """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, mime)

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)

            server.sendmail(sender, receiver, message.as_string())