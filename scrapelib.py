# scrapelib - a simple library to look up student's scores in Bắc Ninh, Việt Nam.
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
import requests
import bs4
import time
from dataclasses import dataclass

_LINK = "http://bacninh.edu.vn/?module=Content.Listing&moduleId=1017&cmd=redraw&site=45610&url_mode=rewrite&submitFormId=1017&moduleId=1017&page=&site=45610"

_DATA = "layout=Decl.DataSet.Detail.default&itemsPerPage=1000&pageNo=1&service=Content.Decl.DataSet.Grouping.select&itemId=6476c98b5fe86d643107bbc4&gridModuleParentId=17&type=Decl.DataSet&page=&modulePosition=0&moduleParentId=-1&orderBy=&unRegex=&keyword={sbd}&_t={timestamp}"
_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "be=73; AUTH_BEARER_default=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2ODY1ODM5MjUsImp0aSI6IkVlOG1XME5pS2h4bDJxS2RqQ0JOeGk2dCt1S0NUVDNpQ2RkZG9BdWJNaWc9IiwiaXNzIjoiYmFjbmluaC5lZHUudm4iLCJuYmYiOjE2ODY1ODM5MjUsImV4cCI6MTY4NjU4NzUyNSwiZGF0YSI6ImNzcmZUb2tlbnxzOjY0OlwiOGNiNGNjZmIyZDU2Y2ViMWQyZGM4ZWU5MzFkMWZiMzI2NDZkZGE4ZWU4MTQ0Y2UwOTJjYmMzODNjNmU2NTIyMlwiO2d1ZXN0SWR8czozMjpcImIzZjk2OWY1Zjk3OTIxODk3MDFkYTZiYTQwMGI4NzkwXCI7dmlzaXRlZDQ1NjEwfGk6MTY4NjU4Mzc0MTsifQ.GtcxUqnQTryx31j4CZH0xU-6OZ6uIogeE1Sfrgvb6OFP18-z5cdUrucu3bGm2QHITuLvz3fDOQ8MyaGrCK8g9A",
    "Host": "bacninh.edu.vn",
    "Origin": "http://bacninh.edu.vn",
    # Warning: link subject to change vvvvvvvvvvvvvvvvvvv
    "Referer": "http://bacninh.edu.vn/tra-cuu/bang-diem-2023",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


@dataclass
class StudentResult:
    schoolID: str
    school_dkdt: str
    sbd: str
    name: str
    sex: str
    birthdate: str
    place_of_bith: str
    class_name: str
    school: str
    uu_tien: int
    van: int
    anh: int
    toan_tl: int
    toan_tn: int
    toan: int
    daitra: int
    kk: int
    chuyen_mon: int
    mchuyen: int
    chuyen: int

    def to_dict(self):
        return {
            "schoolID": self.schoolID,
            "school_dkdt": self.school_dkdt,
            "sbd": self.sbd,
            "name": self.name,
            "sex": self.sex,
            "birthdate": self.birthdate,
            "place_of_bith": self.place_of_bith,
            "class_name": self.class_name,
            "school": self.school,
            "uu_tien": self.uu_tien,
            "van": self.van,
            "anh": self.anh,
            "toan_tl": self.toan_tl,
            "toan_tn": self.toan_tn,
            "toan": self.toan,
            "daitra": self.daitra,
            "kk": self.kk,
            "chuyen_mon": self.chuyen_mon,
            "mchuyen": self.mchuyen,
            "chuyen": self.chuyen,
        }

    def to_beautiful_dict(self):
        return {
            "Mã trường": self.schoolID,
            "Trường đăng kí dự thi": self.school_dkdt,
            "Số báo danh": self.sbd,
            "Họ và tên": self.name,
            "Giới tính": self.sex,
            "Ngày sinh": self.birthdate,
            "Nơi sinh": self.place_of_bith,
            "Lớp": self.class_name,
            "Trường": self.school,
            "Điểm ưu tiên": self.uu_tien,
            "Văn": self.van,
            "Anh": self.anh,
            "Toán tự luận": self.toan_tl,
            "Toán trắc nghiệm": self.toan_tn,
            "Tổng toán": self.toan,
            "Tổng đại trà": self.daitra,
            "Điểm khuyến khích": self.kk,
            "Môn chuyên": self.chuyen_mon,
            "Điểm chuyên": self.mchuyen,
            "Tổng chuyên": self.chuyen,
        }


def lookup(so_bao_danh: str) -> StudentResult:
    """Look up a student's result from their ID.

    #### Parameters
    `so_bao_danh`    the student's ID number

    #### Returns
    `StudentResult` an object contaning the student's exam result.
    """
    # Warning: link subject to change vvvvvvvvvvvvvvvvvvv

    r = requests.post(
        _LINK,
        headers=_HEADERS,
        data=_DATA.format(sbd=so_bao_danh, timestamp=int(time.time())),
    )
    soup = bs4.BeautifulSoup(r.content, features="lxml")

    def proc_result():
        t = soup.find_all("td")
        output = []
        for i in t:
            b = str(i).replace("<td>", "").replace("</td>", "").strip()
            if b.isnumeric() and b[0] != "0":
                output.append(int(b))
            else:
                output.append(b)
        return output

    return StudentResult(*proc_result())
