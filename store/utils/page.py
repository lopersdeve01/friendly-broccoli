

from django.utils.safestring import mark_safe


class DQPage:

    def __init__(self,current_page_number,total_count,per_page_count=10,page_number_show=7,recv_data=None):
        """
        :param current_page_number:   当前页码
        :param total_count:    总数据量
        :param per_page_count:    每页显示多少条
        :param page_number_show:   总共显示多少个页码

        start_page_number:起始页码
        end_page_number:结束页码
        """
        self.recv_data = recv_data

        try:
            current_page_number = int(current_page_number)
        except Exception:
            current_page_number = 1

        half_number = page_number_show // 2
        a, b = divmod(total_count, per_page_count)
        # 如果余数不为0，页码总数为商+1
        if b:
            total_page_count = a + 1
        else:
            total_page_count = a
        # total_page_count 最大页数

        # 如果当前页码大于等于总页数,将当前页面赋值为总页数
        if current_page_number >= total_page_count:
            current_page_number = total_page_count

        # 当当前页码小于等于0的时候，默认显示第一页
        if current_page_number <= 0:
            current_page_number = 1

        # current_page_number 2
        start_page_number = current_page_number - half_number  #
        end_page_number = current_page_number + half_number + 1  # 6

        if start_page_number <= 0:
            start_page_number = 1
            end_page_number = page_number_show + 1  # 7

        if end_page_number >= total_page_count:  # 6 > 2
            start_page_number = total_page_count - page_number_show + 1  # -4
            end_page_number = total_page_count + 1  # 3

        if total_page_count < page_number_show:
            start_page_number = 1
            end_page_number = total_page_count + 1

        self.current_page_number = current_page_number
        self.per_page_count = per_page_count
        self.total_page_count = total_page_count
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number

    @property
    def start_data_number(self):

        return (self.current_page_number - 1) * self.per_page_count

    @property
    def end_data_number(self):

        return self.current_page_number*self.per_page_count

    def page_html_func(self):

        page_html = """
                   <nav aria-label="Page navigation">
                     <ul class="pagination">

                   """
        self.recv_data['page'] = 1
        first_page = f"""
                       <li>
                         <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                           <span aria-hidden="true">首页</span>
                         </a>
                       </li>"""
        page_html += first_page

        self.recv_data['page'] = self.current_page_number - 1
        previous_page = f"""
                   <li>
                         <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                           <span aria-hidden="true">&laquo;</span>
                         </a>
                       </li>"""
        page_html += previous_page

        for i in range(self.start_page_number,self.end_page_number):
            self.recv_data['page'] = i  #
            #<QueryDict: {'search_field': ['qq__contains'], 'keyword': ['123'],'page':'1'}>
            #page=2&search_field=qq__contains&keyword=12
            if i == self.current_page_number:

                page_html += f'<li class="active"><a href="?{self.recv_data.urlencode()}">{i}</a></li>'
            else:
                # page=2&search_field=qq__contains&keyword=123
                # page_html += f"""<li><a href="?page={i}&{ self.recv_data.urlencode().replace('page='+str(self.current_page_number)+'&','') if 'page=' in self.recv_data.urlencode() else self.recv_data.urlencode() }">{i}</a></li>"""
                page_html += f"""<li><a href="?{self.recv_data.urlencode()}">{i}</a></li>"""


        self.recv_data['page'] = self.current_page_number + 1
        next_page = f"""
                       <li>
                             <a href="?{self.recv_data.urlencode()}" aria-label="Next">
                               <span aria-hidden="true">&raquo;</span>
                             </a>
                           </li>
           """
        page_html += next_page

        self.recv_data['page'] = self.total_page_count
        last_page = f"""
                           <li>
                             <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                               <span aria-hidden="true">尾页</span>
                             </a>
                           </li>"""
        page_html += last_page

        page_html += """

                         </ul>
                       </nav>
                   """
        return mark_safe(page_html)








