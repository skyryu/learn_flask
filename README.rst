--------------------------------
This project is the implementation of Plurasight course: Introduction to the Flask Microframework (2014 Dec by Reindert Ekker)

Environment set up:
To view sqllite db file, I use SQL Lite Studio 3.1.1

20180114
pip install Flask-Script
flask.ext.script is deprecated, use flask_script package instead.

20180116
add user page.

20180121
conda install flask-login
add login validation and login page

20180131
add current_user and logout function
in flask_login 0.4.1 the is_authenticated is a property instead of a method, so
we should use current_user.is_authenticated instead of current_user.is_authenticated().

add password authentication.

---------------------------------
20180214
check WTForm validation method to see how the implementation of in-line
validator at: wtforms/wtforms/form.py

def validate(self):
    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
    extra = {}
    for name in self._fields:
        inline = getattr(self.__class__, 'validate_%s' % name, None)
        if inline is not None:
            extra[name] = [inline]

    return super(Form, self).validate(extra)

----------------------------
20180214
Valentine's day.

pip install flask-moment

----------------------------
20180215
re-arrange the layout of the bookmark list into bookmark_list.html.
modify the css for bookmark_list.html in main.css

---------------------------
20180216

Importing flask.ext.moment is deprecated, use flask_moment instead.

---------------------------
20180509

many thing happened during these 3 month since the last time I come. sad
things. new start.

pip install flask-migrate
flask.ext.migrate is deprecated, use flask_migrate instead.

---------------------------
20180510

add Tag table in models.py
add Tag in view and templates.

--------------------------
20180514
create environment.yaml by using(suggested):
    conda env export > environment.yaml
this can be share in other env by using:
    conda env update -f=/path/to/environment.yml

create requirement.txt by using(if don't have conda):
    pip freeze > requirement.txt
this can be shared in other env by using:
    pip install -r /path/requirements.txt

-------------------------
20180626
fix a bug for bookmark_list.html about the tags.

------------------------
20180702
add a @app.context_processor to provide a gloabal accessible dictionary.
add a new route in the view.py for tag. pending to tag.html to be create.


------------------------
20180715

these days I go through the basic of Javascript, finish the book: JS OO
programming guide. As we are going to use select2 which is a JS lib.

select2 suggests we use bower as installer. And bower suggests using npm as
installer. So:
1) go to nodejs.org to download Nodejs for Mac, then the npm is availabe.
2) init bower under /static/ by using cmd: bower init; then you can see the
bower.json is created under the folder.
3) use bower to install select2: bower install select2 --save; this will add
the select2 into /static/bower_components/ folder, and the select2 dependency can be
found in the /static/bower.json

adding a style block in base.html, the bookmark_form.html extends it with
super() to extend the css style.

adding a script block in base.html, the bookmark_form.html extends it to
support select2.

-----------------------
20180721

add select2 js lib for bookmark_form.html.
the tags field in bookmark_form.html uses <input> to integrate with select2
which is already deprecated. Now we need to use <select> to coordinate with select2 v4.0

as SelectMultipleField will check the choices list which doesn't support
editable <select>, I extend a new Select2MultipleField class to dynamically
expand the choice list. this works fine with the tagging feature of Select2.js

-----------------------
20180727
fix the select2 container width issue. set up width='style' to make use of
<select> tag's style attribute.

adding a delete link in bookmark_form.html, adding the corresponding view.
adding confirm_delete.html. Extract out the bookmark.html from
bookmark_list.html for reuse.

----------------------
20180811
server depolyment: apply an AWS EC2 for free.
install nginx. the AWC EC2 uses GNU/Linux which use yum repository for nginx.
so need to set up its repo config in /etc/yum.repos.d/nginx.repo:

    [nginx]
    name=nginx repo
    baseurl=http://nginx.org/packages/OS/OSRELEASE/$basearch/
    gpgcheck=0
    enabled=1

here the OS I choose CentOS.
see link: http://nginx.org/en/linux_packages.html

after yum install nginx, you can: sudo service nginx start
if you see below alert, it means that you need the root role, try sudo.

    nginx: [alert] could not open error log file: open() "/var/log/nginx/error.log" 
        failed (13: Permission denied)
    2018/08/09 15:43:40 [warn] 2771#0: the "user" directive makes sense only if the 
        master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:5
    2018/08/09 15:43:40 [emerg] 2771#0: mkdir() "/var/lib/nginx/tmp/client_body" 
        failed (13: Permission denied)

after the nginx starts, you can access the nginx welcome page throught the aws
ec2 public IP. if you find an error 404 then it might due to you haven't
correctly configure your security group of your ec2 instance.
by default, the in-bound rule only contains the SSH protocal at port:22. you need to
manually add the HTTP protocal at 80 port to enable browser connect. 

---------------------
20180812
copy a virtual environment from learn_flask:
    # To activate this environment, use:
    # > source activate /Users/hongjin/conda_env/test_env_cp
    #
    # To deactivate an active environment, use:
    # > source deactivate
the cmd used to copy the virtual environment:
    conda env [create|update] -f=./environment.yaml -p /Users/hongjin/conda_env/test_env_cp

Part of the packages in environment.yaml are downloaded by pip.
I can't find a way to set the pip source in conda, the conda channel is a
different thing from pip source. so when conda try to download packages using
pip from the default pip source you may get time out socket error.

I find a bypass to fix this issue by adding the pip source 
in a global config file under: ~/.pip/pip.conf with content:
    [global]
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple
    [install]
    trusted-host=mirrors.aliyun.com

in the ec2 us instance I expect the default pip source should be enough and the
tsinghua pip source will become very slow as located in China.

---------------------
20180901
create new conda environment: deploy_env for web server deployment
create fabfile.py from deployment automation.
pip install fabric(v2.3.1) & Invocations (The invocations pkg provides the console
confirm function)


