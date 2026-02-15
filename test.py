data_sample = """

> || Breakfast || Oats || 0.2 || 300 > 
> || Lunch || Biriyani || 10 || 300 > 
> ||  Dinner || Roti || 0 || 400 > 

    """

s = data_sample.split(">")
out = []
for x in s:
    if x.strip().startswith("||"):
        h = x.split("||")[1::]
        m,n,p,c = h
        out.append([m.strip(),n.strip(),p.strip(),c.strip()])
print(out)
