def run(text):
    import json
    import re
    print(text)
    clean_response = re.sub(r'//.*', '', text)
    print(clean_response)
    out = []
# Parse the JSON string into a dictionary
    a = True
    if a :
        data = json.loads(clean_response)
    else:
        data_sample = """

> Breakfast || Oats || 0.2 || 300 
> Lunch || Biriyani || 10 || 300
> Dinner || Roti || 0 || 400 

    """

        s = data_sample.split(">")
        out = []
        for x in s:
            if x.strip().startswith("||"):
                h = x.split("||")[1::]
                m,n,p,c = h
                out.append([m.strip(),n.strip(),p.strip(),c.strip()])
        print(out)

    return out
    print(data)



    