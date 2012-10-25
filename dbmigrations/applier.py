def initOptionParser(parser):
    parser.add_argument("-d","--db","--database",dest="database",help="Specify the database name.")
    parser.add_argument("-h","--host","--hostname",dest="hostname",help="Specify the database hostname.")
    parser.add_argument("-p","--port",dest="port",help="Specify the database port.")
    parser.add_argument("-U","--user","--username",dest="username",help="Specify the database username.")

def main(args):
    if(args.help):
        args.parser.print_help()
        return
    print args
    print("Apply...")

class MigrationCreater:
    pass    
