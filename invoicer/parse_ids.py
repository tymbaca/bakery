from pprint import pprint


def parse_ids(input_filename: str, output_filename: str):
    ids = _parse_ids(input_filename)
    save_result(output_filename, ids)


def _parse_ids(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        lines = f.readlines()

    ids: list[list[str]] = []
    current_day_index = -1
    for line in lines:
        if "#" in line:
            ids.append([])
            current_day_index += 1
        if "-" in line:
            try:
                splited_line = line.split()
                id = splited_line[-1]
                if "-" in id:
                    id = id.replace("-", "")
               
                ids[current_day_index].append(id)
            except Exception as err:
                print(line)
                print(splited_line)
                raise err
    
    return ids
    

def save_result(filename: str, ids):
    with open(filename, "w") as file:
        for day in ids:
            for id in day:
                file.write(id + " ")
            file.write("\n")

if __name__ == "__main__":
    ids = _parse_ids("target.md")
    save_result("result.md", ids)
