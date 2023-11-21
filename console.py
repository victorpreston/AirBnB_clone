#!/usr/bin/python3
"""
Airbnb Console
"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.state import State


class HBNBCommand(cmd.Cmd):
    """
    The entry point for the command interpreter
    """
    prompt = '(hbnb) '
    classes = ['BaseModel', 'User', 'Place', 'State',
               'City', 'Amenity', 'Review']
    dotcmds = ['.all()', '.count()']

#   def parseline(self, line):
#       print (f'parseline({line}) =>')
#       ret = cmd.Cmd.parseline(self, line)
#       print (ret)
#       return ret

    def do_create(self, line):
        """Creates a new instance of a given class, saves it \
(to the JSON file) and prints the id."""
        if line == '':
            print('** class name missing **')
        elif line not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if line == 'BaseModel':
                obj = BaseModel()
            elif line == 'User':
                obj = User()
            elif line == 'Place':
                obj = Place()
            elif line == 'State':
                obj = State()
            elif line == 'City':
                obj = City()
            elif line == 'Amenity':
                obj = Amenity()
            elif line == 'Review':
                obj = Review()
            storage.save()
            print(obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance based \
on the class name and id."""
        args = line.split()
        if line == '':
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objid = args[1]
                key = classname + '.' + objid
                try:
                    print(storage.all()[key])
                except KeyError:
                    print('** no instance found **')

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file)
        """
        args = line.split()
        if line == '':
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objid = args[1]
                key = classname + '.' + objid
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

    def do_all(self, line):
        """
        Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all
        """
        args = line.split()
        result = []
        if len(args) != 0:
            if args[0] not in HBNBCommand.classes:
                print('** class doesn\'t exist **')
                return
            else:
                for key, value in storage.all().items():
                    if type(value).__name__ == args[0]:
                        result.append(value.__str__())
        else:
            for key, value in storage.all().items():
                result.append(value.__str__())
        print(result)

    def do_update(self, line):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file). Ex: $ update
        BaseModel 1234-1234-1234 email "aibnb@mail.com".
        update <class name> <id> <attribute name> "<attribute value>"
        """
        args = line.split()
        if line == '':
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        elif len(args) < 2:
            print('** instance id missing **')

        elif len(args) < 3:
            print('** attribute name missing **')
        elif len(args) < 4:
            print('** value missing **')
        else:
            classname = args[0]
            objid = args[1]
            attr = args[2]
            value = args[3]
            oob = ['id', 'created_at', 'updated_at']
            if attr in oob:
                print('** attribute can\'t be updated **')
                return
            """
            string validity test begins (incomplete)
            """
            if value[0] == '"' and value[-1] == '"' or value[0] == "'":
                if value[0] != '"':
                    print("** A string argument must be between \
double quotes **")
                    return
                value = value[1:-1]
            else:
                try:
                    for c in value:
                        if c == '.':
                            value = float(value)
                            break
                    else:
                        value = int(value)
                except ValueError:
                    print("** A string argument must \
be between double quote **")
            if (attr[0] == '"' and attr[-1] == '"')\
               or attr[0] == "'" or attr[-1] == "'":
                if attr[0] != '"' or attr[-1] == "'":
                    print("** A string argument must be between \
double quotes **")
                    return
                attr = attr[1:-1]
            """ string validity test ends """
            key = classname + '.' + objid
            try:
                instance = storage.all()[key]
                instance.__dict__[attr] = value
                instance.save()
            except KeyError:
                print('** no instance found **')

    def do_BaseModel(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'BaseModel':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'BaseModel.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'BaseModel.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'BaseModel.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_User(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'User':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'User.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'User.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'User.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_Place(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Place':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Place.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'Place.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Place.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_State(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'State':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'State.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'State.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'State.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_City(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'City':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'City.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'City.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'City.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_Amenity(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Amenity':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Amenity.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'Amenity.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Amenity.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_Review(self, line):
        objects = []
        parse_line = cmd.Cmd.parseline(self, line)
        arg = parse_line[2]

        for key, value in storage.all().items():
            if type(value).__name__ == 'Review':
                objects.append(value)

        if arg in HBNBCommand.dotcmds:
            result = [value.__str__() for value in objects]
            if arg == HBNBCommand.dotcmds[0]:
                print(result)
            elif arg == HBNBCommand.dotcmds[1]:
                print(len(result))

        elif arg[0:6] == '.show(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[6:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                for obj in objects:
                    if obj.id == model_id:
                        print(obj)
                        break
                else:
                    print('** no instance found **')

        elif arg[0:9] == '.destroy(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                model_id = arg[9:-1]
                if model_id == '':
                    print("** instance id missing **")
                    return
                key = 'Review.' + model_id
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

        elif arg[0:8] == '.update(':
            if arg[-1] != ')':
                return cmd.Cmd.default(self, line)
            else:
                args = arg[8:-1]
                args_list = args.split(',')
                oob = ['id', 'created_at', 'updated_at']

                if len(args_list) < 2 and args_list[0] == '':
                    print('** instance id missing **')
                    return
                elif len(args_list) < 2:
                    print('** attribute name missing **')
                    return
                else:
                    # clear whitespaces around arguments
                    i = 0
                    while (i < len(args_list)):
                        while(args_list[i][0] == " "):
                            args_list[i] = args_list[i][1:]
                        i += 1

                    if args_list[1][0] == '{' and args_list[-1][-1] == '}':
                        dictargs = args_list[1:]
                        dictargs[0] = dictargs[0][1:]
                        dictargs[-1] = dictargs[-1][:-1]
                        key = 'Review.' + args_list[0]
                        try:
                            instance = storage.all()[key]
                        except KeyError:
                            print('** no instance found **')
                            return
                        for s in dictargs:
                            keyval = s.split(':')
                            key = keyval[0]
                            value = keyval[1]
                            while(value[0] == " "):
                                value = value[1:]
                            if key in oob:
                                print('** attribute can\'t be updated **')
                                return
                            if (key[0] == '"' and key[-1] == '"')\
                               or (key[0] == "'" and key[-1] == "'"):
                                key = key[1:-1]
                            else:
                                print("** Dictionary object keys must be \
strings **")
                                return
                            if (value[0] == '"' and value[-1] == '"')\
                               or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]

                            else:
                                for c in value:
                                    if c == " ":
                                        print("** A string argument with a \
space must be between double quotes **")
                                        return
                                try:
                                    for c in value:
                                        if c == '.':
                                            value = float(value)
                                            break
                                    else:
                                        value = int(value)
                                except ValueError:
                                    pass

                            instance.__dict__[key] = value
                            instance.save()
                        return
                    elif len(args_list) < 3:
                        print('** value missing **')
                        return

                model_id = args_list[0]
                attr = args_list[1]
                value = args_list[2]

                if attr in oob:
                    print('** attribute can\'t be updated **')
                    return
                """
                string validity test begins (incomplete)
                """
                if (attr[0] == '"' and attr[-1] == '"'):
                    attr = attr[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    for i in attr:
                        if i == " ":
                            print("** A string argument with a space \
must be between double quotes **")
                            return
                    try:
                        for c in value:
                            if c == '.':
                                value = float(value)
                                break
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                """ string validity test ends """

                key = 'Review.' + model_id
                try:
                    instance = storage.all()[key]
                    instance.__dict__[attr] = value
                    instance.save()
                except KeyError:
                    print('** no instance found **')

        else:
            return cmd.Cmd.default(self, line)

    def do_quit(self, line):
        """Quit command to exit from cmd"""
        return True

    def do_EOF(self, line):
        """Ctrl D - to kill the program or exit from cmd"""
        print()
        return True

    def emptyline(self):
        """Empty line + Enter shouldn't execute anything"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
