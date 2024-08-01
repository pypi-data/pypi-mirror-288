from urllib.parse import urlparse, quote_plus, unquote

#print("load " + '/'.join(__file__.split('/')[-2:]))

class URLParseResult():
    def __init__(self, Schema:str, Host:str, Port:int, User:str, Pass:str, Path:str, Query:str, Fragment:str):
        self.Schema = Schema
        self.Host = Host    
        self.Port = Port    
        self.User = User    
        self.Pass = Pass    
        self.Path = Path    
        self.Query = Query   
        self.Fragment = Fragment
    
    def __repr__(self):
        return f"URLParseResult(Schema={self.Schema}, Host={self.Host}, Port={self.Port}, User={self.User}, Pass={self.Pass}, Path={self.Path}, Query={self.Query}, Fragment={self.Fragment})"

    def __str__(self):
        return f"URLParseResult(Schema={self.Schema}, Host={self.Host}, Port={self.Port}, User={self.User}, Pass={self.Pass}, Path={self.Path}, Query={self.Query}, Fragment={self.Fragment})"

class URL():
    def __init__(self, url:str):
        self.url = url 
    
    def Parse(self) -> URLParseResult:
        """
        It parses the URL and returns the URLParseResult object.
        :return: A URLParseResult object.
        """
        # 有时候是 example.com/abc?key=value, 这样没法解析, 所以加一个头才能解析
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            url = 'http://' + self.url 
        else:
            url = self.url 

        res = urlparse(url)

        # 如果是自己加的协议头, 就不写到schema里面了
        if url == self.url:
            Schema = res.scheme
        else:
            Schema = None
        Path = res.path
        Query = res.query 
        Fragment = res.fragment

        if '@' not in res.netloc:
            User = None
            Pass = None
        else:
            u = res.netloc.split("@")[0]
            if ':' in u:
                User = u.split(":")[0]
                Pass = u.split(":")[1]
            elif len(u) != 0:
                User = u 
                Pass = None
            else:
                User = None 
                Pass = None
        # print(res)
        h = res.netloc 
        if '@' in res.netloc:
            h = res.netloc.split("@")[1]
        
        if ':' not in h:
            Host = h 
            if Schema == "http":
                Port = 80
            elif Schema == "https":
                Port = 443 
            else:
                Port = None
        else:
            Host = h.split(":")[0]
            Port = int(h.split(":")[1])
        
        return URLParseResult(Schema, Host, Port, User, Pass, Path, Query, Fragment)
    
    def Encode(self) -> str:
        return quote_plus(self.url)
    
    def Decode(self) -> str:
        return unquote(self.url)

if __name__ == "__main__":
    # u = URL("http://user:pass@docs.python.org:8897/3/library/urllib.parse.html?highlight=params&k=v#url-parsing")
    # print(u.Parse())

    # u = URL("example.com?title=правовая+защита")
    # print(u.Encode())

    # u = URL(u.Encode())
    # print(u.Decode())

    # u = URL("example.com/abc?key=value")
    # print(u.Parse())

    u = URL("ss://YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU@54.95.169.40:443#%e6%97%a5%e6%9c%ac%3dtg%e9%a2%91%e9%81%93%3a%40bpjzx2%3d1")
    print(u.Parse())