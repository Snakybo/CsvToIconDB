import sys

addon_namespace = ""
addon_function = "GetIcons"
addon_create = False
listfile = ""
output = ""
blacklist = ""

blacklist_parsed = {}

def parse_args():
	global listfile
	global output
	global blacklist
	global addon_namespace
	global addon_function
	global addon_create

	for i in range(1, len(sys.argv)):
		current = sys.argv[i]
		next = ""

		if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
			next = sys.argv[i + 1]

		if current == "--input":
			listfile = next
		elif current == "--output":
			output = next
		elif current == "--blacklist":
			blacklist = next
		elif current == "--namespace":
			addon_namespace = next
		elif current == "--create-addon":
			addon_create = bool(next) if next != "" else True
		elif current == "--function":
			addon_function = next

def parse_blacklist():
	global blacklist_parsed

	if blacklist == "":
		return

	print("Reading icon blacklist from: " + blacklist)

	try:
		with open(blacklist, "r", encoding = "utf8") as f:
			blacklist_parsed = [line.rstrip() for line in f]
			print("Parsed " + str(len(blacklist_parsed)) + " blacklist item(s)")
	except Exception as fserr:
		print("Unable to read blacklist: " + blacklist + ": " + str(fserr))
		sys.exit(1)

def is_valid_icon_file(fd_id, path):
	p = path.lower()

	if not p.startswith("interface\\icons\\") or not p.endswith(".blp"):
		return False

	if fd_id in blacklist_parsed:
		return False

	return True

def strip_path(path):
	parts = path.split("/")
	filename = parts[len(parts) - 1]

	parts = filename.split(".")
	return parts[0]

def write_output():
	global listfile
	global output

	print("Writing icon data from " + listfile + " to " + output)

	if addon_namespace == "":
		print("No addon namespace specified, specify one using the --namespace parameter")
		sys.exit(1)

	if addon_function == "":
		print("No addon function specified, specify one using the --function parameter")
		sys.exit(1)

	num_icons = 0

	try:
		listfile_fs = open(listfile, "r", encoding = "utf8")
		output_fs = open(output, "w", encoding = "utf8")

		output_fs.write("--- @class " + addon_namespace + "\n")

		if addon_create:
			output_fs.write(addon_namespace + " = LibStub(\"AceAddon-3.0\"):NewAddon(\"" + addon_namespace + "\")\n")
		else:
			output_fs.write(addon_namespace + " = " + addon_namespace + " or {}\n")

		output_fs.write("\n")
		output_fs.write("--- @type table<integer,string>\n")
		output_fs.write("local icons = {\n")

		fd_ids = []

		for line in listfile_fs:
			parts = line.split(",")

			if len(parts) != 3:
				continue

			fd_id = parts[0]
			folder = parts[1].strip()
			file_name = parts[2].strip()
			full_path = folder + file_name

			if not is_valid_icon_file(fd_id, full_path):
				continue

			output_fs.write("\t[" + str(fd_id) + "] = \"" + strip_path(file_name).lower() + "\",\n")
			fd_ids.append(int(fd_id))
			num_icons += 1

		output_fs.write("}\n")

		fd_ids.sort()

		output_fs.write("\n")
		output_fs.write("--- @type integer[]\n")
		output_fs.write("local order = {\n")

		for fd_id in fd_ids:
			output_fs.write("\t" + str(fd_id) + ",\n")

		output_fs.write("}\n")
		output_fs.write("\n")

		output_fs.write("--- @return table<integer,string>\n")
		output_fs.write("--- @return integer[]\n")
		output_fs.write("function " + addon_namespace + ":" + addon_function + "()\n")
		output_fs.write("\treturn icons, order\n")
		output_fs.write("end")
		output_fs.write("\n")

		listfile_fs.close()
		output_fs.close()
	except Exception as fserr:
		print("Unable to write icon data to " + output + ": " + str(fserr))
		sys.exit(1)

	print("Successfully wrote " + str(num_icons) + " icons to: " + output)

parse_args()
parse_blacklist()
write_output()
