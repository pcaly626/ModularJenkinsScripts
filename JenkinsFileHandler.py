import os

class JenkinsFileHandler:

    def GetJenkinsBuildNumber(self, buildFile):
        return int(self.ReadFromFile(buildFile)) - 1

    def GetLogFile(self, path ):
        return os.path.join(path, "log" )

    def WriteToFile( self, input, fileName ):
        resultFile = open( fileName,"w" )
        resultFile.write( input )
        resultFile.close(  )

    def ReadFromFile( self, fileName ):
        resultFile = open( fileName,"r" )
        result = resultFile.read( )
        resultFile.close(  )
        return result