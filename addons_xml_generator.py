from __future__ import with_statement

## repo addons.xml and addons.xml.md5 generator

from xml.dom.minidom import parseString
import hashlib
import os
import sys
import shutil

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """

    def __init__( self ):
        # generate addons.xml file
        if ( not self._generate_addons_xml_file() ):
            sys.exit( 0 )
        # generate addons.xml.md5 file
        if ( not self._generate_addons_xml_md5_file() ):
            sys.exit( 0 )
        # notify user of successfully updating files
        print "Finished updating addons.xml and addons.xml.md5 files!"

    def _generate_addons_xml_file( self ):
        # addons.xml heading block
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        # ignore folders
        ignore_folder = [
            'wiki',
            'zips'
            ]
        # list of only folders, skip special .svn folder
        folders = [ f for f in os.listdir( os.curdir )
                   if ( os.path.isdir( f ) and f != ".svn" and f not in ignore_folder ) ]
        
        # loop thru and add each addons addon.xml to the final addons.xml file
        for folder in folders:
            try:              
                # version
                addonid = ""
                version = ""
                # new addon.xml text holder
                addon_xml = u""
                # create full path to an addon.xml file
                _path = os.path.join( folder, "addon.xml" )
                # split lines for stripping
                with open( _path, "r" ) as addon_file:
                    
                    # loop thru cleaning each line                    
                    for line in addon_file:
                        # skip heading block as we already have one
                        if ( line.find( "<?xml" ) >= 0 ): continue
                        # find addon id
                        if not addonid and line.find( 'id' ) >= 0: 
                            import re
                            addonid = re.search('id=[\'"](.+?)[\'"]', line).group(1)
                        # find the line with version
                        if addonid and not version and line.find( 'version' ) >= 0: 
                            import re
                            version = re.search('version=[\'"](.+?)[\'"]', line).group(1)
                        # add line
                        addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                # check for a properly formatted xml file
                parseString( addon_xml.encode( "UTF-8" ) )
                # zip the directory
                if id:
                    current_directory = os.getcwd()
                    zips_directory = os.path.join( current_directory, 'zips' )
                    directory = os.path.join(zips_directory, addonid)
                    if not os.path.exists( directory ):
                        os.makedirs(directory)

                    icon_png = os.path.join( folder, 'icon.png' )
                    if os.path.exists( icon_png ):
                        shutil.copy(icon_png, directory)

                    fanart_jpg = os.path.join( folder, 'fanart.jpg' )
                    if os.path.exists( fanart_jpg ):
                        shutil.copy(fanart_jpg, directory)

                    changelog_txt = os.path.join( folder, 'changelog.txt' )
                    if os.path.exists( changelog_txt ):
                        shutil.copy(changelog_txt, os.path.join(directory, 'changelog-' + version + '.txt' ))
                        
                    self.zipdir(folder, addonid + '-' + version + '.zip')
                    if os.path.exists( os.path.join(directory, addonid + '-' + version + '.zip') ):
                        os.remove(os.path.join(directory, addonid + '-' + version + '.zip'))
                    shutil.move(addonid + '-' + version + '.zip', directory)
            except Exception as e:
                # missing or malformed addon.xml
                print "* Excluding {path} for {error}".format( path=_path, error=e )
            else:
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # save file and return result
        return self._save_file( data=addons_xml.encode( "UTF-8" ), file="addons.xml" )

    def _generate_addons_xml_md5_file( self ):
        try:
            # create a new md5 hash
            md5 = hashlib.md5( open( "addons.xml" ).read() ).hexdigest()
        except IOError as e:
            # oops
            print "An error occurred creating md5 hash from addons.xml file!\n{error}".format( error=e )
            # return failed
            return False
        else:
            # save file
            return self._save_file( data=md5, file="addons.xml.md5" )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "w" ).write( data )
        except IOError as e:
            # oops
            print "An error occurred saving {file} file!\n{error}".format( file=file, error=e )
            # return failed
            return False
        else:
            # return success
            return True

    def zipdir(self, basedir, archivename):
                
        from contextlib import closing
        from zipfile import ZipFile, ZIP_DEFLATED
        import os

        assert os.path.isdir(basedir)
        zdir = os.path.dirname(basedir)
        with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
            for root, dirs, files in os.walk(basedir):
                #NOTE: ignore empty directories
                for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(zdir):] #XXX: relative path
                    z.write(absfn, zfn)

# start
if ( __name__ == "__main__" ):
    Generator()
	
