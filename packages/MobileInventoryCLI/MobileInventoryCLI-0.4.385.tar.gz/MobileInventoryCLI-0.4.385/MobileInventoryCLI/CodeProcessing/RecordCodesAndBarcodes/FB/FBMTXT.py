fm_data={'Name':{
            'type':'str',
            'default':'',
            },
        'Value':{
            'type':'int',
            'default':0,
            },
        'Price':{
           'type':'float',
           'default':0.0,
            },
        'Barcode':{
            'type':'str',
            'default':'000000000000',
            },
        'Code':{
            'type':'str',
            'default':'12345678',
            },
        'DOE':{
            'type':'date',
            'default':None,
            },
        'TOE':{
            'type':'time',
            'default':None,
            },
        'DTOE':{
            'type':'datetime',
            'default':None,
            },
        'DEFAULT':{
            'type':'bool',
            'default':False,
            },
        'List':{
            'type':'list',
            'default':[],
            },
      }
def FormBuilderMkText(text,data):
    try:
        if text in ['f','m','p','d']:
            return text
        if text == '':
            return 'd'
        value=None
        if data.lower() == 'float':
            try:
                value=float(eval(text))
            except Exception as e:
                try:
                    value=float(text)
                except Exception as e:
                    return 'd'
        elif data.lower() in ['int','integer']:
            try:
                value=int(eval(text))
            except Exception as e:
                try:
                    value=int(text)
                except Exception as e:
                    return 'd'
        elif data.lower() in ['bool','boolean']:
            try:
                value=bool(eval(text))
            except Exception as e:
                try:
                    if text.lower() in ['y','yes','true','t','1']:
                        value=True
                    elif text.lower() in ['n','no','false','f','0']:
                        value=False
                    else:
                        try:
                            value=bool(eval(text))
                        except Exception as e:
                            return 'd'
                except Exception as e:
                    return 'd'
        elif data.lower() in ['str','string',"varchar"]:
            value=text
        elif data.lower() == 'date':
            if text.lower() in ['y','yes','1','t','true']:
                value=DatePkr()
        elif data.lower() == 'time':
            if text.lower() in ['y','yes','1','t','true']:
                value=TimePkr()
        elif data.lower() == 'datetime':
            if text.lower() in ['y','yes','1','t','true']:
                value=DateTimePkr()
        elif data.lower() == 'list':
            splitBy=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Split the String by?",helpText="what character to use to make a list default=,",data="str")
            if splitBy in [None,]:
                value=[]
            elif splitBy == 'd':
                value=text.split(",")
            else:
                value=text.split(splitBy)
        return value
    except Exception as e:
        print(e)