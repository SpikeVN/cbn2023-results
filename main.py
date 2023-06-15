# fetchscore - a simple program to mass look up student's scores in Bắc Ninh, Việt Nam.
# Copyright (C) 2022-2023 Nguyễn Tri Phương
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import time
import pdfkit
import scrapelib
import threading
import pandas
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("./templates"))
template = environment.get_template("bangdiem.html")

students: dict[str, list[scrapelib.StudentResult]] = {}
req = 0

def add(sbd: str, classname: str) -> None:
    global req
    s = scrapelib.lookup(sbd)
    students[classname].append(s)
    req += 1


def do_things(name: str, classname: str):
    global req
    with open(os.path.join("sbd", f"sbd_{classname}.txt"), "r", encoding="utf8") as f:
        t = None
        students[classname] = []
        start = time.perf_counter()
        for l in f.readlines():
            t = threading.Thread(target=add, args=(l.strip(), classname), daemon=True)
            t.start()
        t.join()
        dur = time.perf_counter() - start
        print(f"[SPEED] Tốc độ trung bình: {round(req/dur, 2)} requests/s")
        req = 0

    students[classname].sort(key=lambda x: x.chuyen, reverse=True)
    print(f"    > Đang xuất PDF cho Chuyên {name}")
    pdfkit.from_string(
        template.render(students=list(enumerate(students[classname])), name=name),
        output_path=os.path.join("pdf", f"{classname}.pdf")
    )


if __name__ == "__main__":
    print("[STAGE 1] Đang lấy điểm...")
    for name, classname in {
        "Anh": "anh",
        "Địa": "dia",
        "Hóa": "hoa",
        "Lý": "ly",
        "Sinh": "sinh",
        "Sử": "su",
        "Tin": "tin",
        "Toán": "toan",
        "Văn": "van",
    }.items():
        print(f"[SWITCH] Đang lấy điểm của khối Chuyên {name}")
        do_things(name, classname)
    print("[STAGE 2] Đang xuất CSV")
    for classname, data in students.items():
        pandas.DataFrame([i.to_beautiful_dict() for i in data]).to_csv(os.path.join("csv", f"{classname}.csv"))
        print(f"    > Đã lưu csv/{classname}.csv")

    print("[COMPLETE] Hoàn tất. File dạng PDF được lưu ở pdf/, file dạng CSV được lưu ở csv/.")
