from django.utils.safestring import mark_safe
# 集中处理页面的网页格式

class DQpage:
    def __init__(self,page,obj_num,page_shown_num,page_number,recv_data=None):
        '''
        :param current_page:  当前页码(后端获取当前网页)
        :param obj_num:   总显示对象数量
        :param page_shown_num:  每页显示对象数量
        :param page_number:  下面的分页框现实的标签数量
        start_page:  下面的分页框 起始显示页码
        end_page:     下面的分页框 终止显示页码
        '''

        self.recv_data=recv_data

        # obj_num = obj.count()
        print(obj_num)

        a, b = divmod(obj_num, page_shown_num)
        page_num = a if not b else a + 1
        page_shown_rage = page_number // 2

        try:
            shown_page = int(page) #对获取网页进行验证，验证后当前网页(字符串获取)
        except Exception:
            shown_page = 1

        if shown_page in range(1, page_num + 1):  # show_page验证后的显示网页
            current_page = shown_page             # 显示网页范围校验
        else:
            current_page = 1

        if current_page - page_shown_rage <= 0:   # 起始与终止网页控制
            start_page = 1
            if current_page + page_shown_rage + 1 >= page_num + 1:
                end_page = page_num + 1
            else:
                end_page = current_page + page_shown_rage + 1
        else:
            start_page = current_page - page_shown_rage
            if current_page + page_shown_rage + 1 >= page_num + 1:
                end_page = page_num + 1
            else:
                end_page = current_page + page_shown_rage + 1

        start_obj = (current_page - 1) * page_shown_num  # 获取显示对象范围
        if (current_page) * page_shown_num + 1 >= obj_num + 1:
            end_obj = obj_num + 1
        else:
            end_obj = (current_page) * page_shown_num + 1


        # obj1 = obj[start_obj:end_obj]

        lst = range(start_page, end_page)
        print(lst)
        if current_page == 1:
            pre = 1
        else:
            pre = current_page - 1
        if current_page == page_num:
            next = page_num
        else:
            next = current_page + 1


        # 封装属性
        self.current_page=current_page
        self.end_page=obj_num + 1
        self.pre=pre
        self.next=next
        self.start_obj=start_obj
        self.end_obj=end_obj

        #
        #
        # @property
        # def start_obj(self):
        #
        #     return (self.current_page - 1) * self.page_shown_num
        #
        # @property
        # def end_objr(self):
        #
        #     return self.current_page * self.page_shown_num

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

        self.recv_data['page'] = self.pre
        previous_page = f"""
                      <li>
                            <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                              <span aria-hidden="true">&laquo;</span>
                            </a>
                          </li>"""
        page_html += previous_page

        for i in range(self.start_obj, self.end_obj):
            self.recv_data['page'] = i  #
            # <QueryDict: {'search_field': ['qq__contains'], 'keyword': ['123'],'page':'1'}>
            # page=2&search_field=qq__contains&keyword=12
            if i == self.current_page:

                page_html += f'<li class="active"><a href="?{self.recv_data.urlencode()}">{i}</a></li>'
            else:
                # page=2&search_field=qq__contains&keyword=123
                # page_html += f"""<li><a href="?page={i}&{ self.recv_data.urlencode().replace('page='+str(self.current_page_number)+'&','') if 'page=' in self.recv_data.urlencode() else self.recv_data.urlencode() }">{i}</a></li>"""
                page_html += f"""<li><a href="?{self.recv_data.urlencode()}">{i}</a></li>"""

        self.recv_data['page'] = self.next
        next_page = f"""
                          <li>
                                <a href="?{self.recv_data.urlencode()}" aria-label="Next">
                                  <span aria-hidden="true">&raquo;</span>
                                </a>
                              </li>
              """
        page_html += next_page

        self.recv_data['page'] = self.end_page
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


