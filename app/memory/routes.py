from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required

from wtforms import StringField, SubmitField

from app import db
#from app.main.forms import EditProfileForm, PostForm
from app.memory.forms import NewMemoryForm, EditMemoryForm, ForgetForm
from app.models import User, Memory, Tag, MemoryTag
from app.memory import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        current_app.logger.info(page.args)

    memories = current_user.get_memories().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    
    current_app.logger.info('user is: {}'.format(current_user.username))
    current_app.logger.info('output memories: {}'.format(current_user.get_memories()))

    next_url = url_for('memory.index', page=memories.next_num) \
        if memories.has_next else None
    prev_url = url_for('memory.index', page=memories.prev_num) \
        if memories.has_prev else None

    return render_template('memory/index.html', title='Memories',
                           memories=memories.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/forget', methods=['GET', 'POST'])
@login_required
def forget():
    form = ForgetForm()
    memory_id = request.args.get('id')
    memory = Memory.query.get(memory_id)
    if form.validate_on_submit():
#        current_app.logger.info('keep button return value {}'.format(form.keep.data))
#        current_app.logger.info('forget button return value {}'.format(form.forget.data))
        if form.forget.data:
            # forget
            current_app.logger.info('forgotten: {}'.format(request.args.get('id')))
            flash('this memory is gone')
            memory.dormant=True
            db.session.commit()
            flash('Memory is forgotten')
            return redirect(url_for('memory.index'))
        elif form.keep.data:
            # keep
            flash('keep this memory')    
            return redirect(url_for('memory.index'))
        else:
            current_app.logger.info('this should not happen')
    elif request.method=='GET':
        # come here when form needs to be populated with database info
        form.id.data = memory.id
        form.type.data = memory.type
        form.category.data = memory.category
        form.abstract.data = memory.abstract
        form.tags.data = ','.join(memory.get_taglist())
        form.posted.data = memory.get_datestring()

    return render_template('memory/forget.html', title='Forget or not forget', form=form, memory=memory)


"""
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
"""
@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    # get existing memory
    memory_id = request.args.get('id')
    memory = Memory.query.get(memory_id)
    change_detected = False

    # create a memory form to be populated
    form = EditMemoryForm()
    # apply changes
    if form.validate_on_submit():
        orig_taglist = memory.get_taglist()
        if form.memorize.data:
            if memory.type != form.type.data:
                change_detected = True
                memory.type = form.type.data
            if memory.category != form.category.data:
                change_detected = True
                memory.category = form.category.data
            if memory.abstract != form.abstract.data:
                change_detected = True
                memory.abstract = form.abstract.data        
            taglist = form.tags.data.replace(' ','').replace(';',',').split(',')
            if memory.get_taglist() != taglist:
                change_detected = True
            # check if tag is new, in Tag table directly, if yes add together with relationship
                for item in taglist:
                    if Tag.query.filter(Tag.tag==item).first() is None:
                        # new tag ... write to Tag table and remember tag.id
                        tag_in = Tag(tag=item)
                        db.session.add(tag_in)
                        db.session.flush()
                        tag_id = tag_in.id       #Tag.query.filter(Tag.tag==item).first()
                        current_app.logger.info( 'edit: added new tag {} to db with id {}'.format(item,tag_id) )
                        # tag is new so add memory-tag relation to db and flush
                        db.session.add(MemoryTag(memory_id=memory_id,tag_id=tag_id))
                        db.session.flush()
                    else:
                        # tag alrerady exists so get tag.id from db
                        tag_id = Tag.query.filter(Tag.tag==item).first().id
                        # now check if the relation memory-tag already exists, if not then add
                        if MemoryTag.query.filter(MemoryTag.memory_id==memory_id, MemoryTag.tag_id==tag_id).first() is None:
                            db.session.add(MemoryTag(memory_id=memory_id,tag_id=tag_id))
                            db.session.flush()
                # now check if items were removed
                for item in orig_taglist:
                    if item not in taglist:
                        # remove relationship in MemoryTag
                        change_detected=True
                        tag_id = Tag.query.filter(Tag.tag==item).first().id
                        current_app.logger.info('remove relationship {}:{}'.format(memory_id,tag_id))
                        mtd = MemoryTag.query.filter(MemoryTag.memory_id==memory_id, MemoryTag.tag_id==tag_id).first()
                        db.session.delete(mtd)
                        db.session.flush() 
            if change_detected:
                memory.timestamp = datetime.now()
                db.session.commit()
        return redirect(url_for('memory.index'))            
    # at start show entries from db
    elif request.method == 'GET':
        form.id.data = memory.id
        form.type.data = memory.type
        form.category.data = memory.category
        form.abstract.data = memory.abstract
        form.tags.data = ','.join(memory.get_taglist())
        form.posted.data = memory.get_datestring()
    else:
        pass # raise some error
    return render_template('memory/edit_memory.html', title='Remember and Rethink', form=form, memory=memory)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    
    setattr(NewMemoryForm, 'source', StringField('Source'))
    setattr(NewMemoryForm, 'source_url', StringField('Source URL'))
    setattr(NewMemoryForm, 'submit', SubmitField('Remember this'))

    form = NewMemoryForm()
    jsondoc={}
    
    if form.validate_on_submit():
        jsondoc['source'] = form.source.data
        jsondoc['source_url'] = form.source_url.data
        memory = Memory(type=form.type.data, 
                        category=form.category.data,
                        abstract=form.abstract.data,
			            doc=jsondoc,
                        user_id=current_user.id,
                        memorized=datetime.now())
        db.session.add(memory)
        db.session.commit()
        flash('New memory created!')

        # add tags to list
        memory_id = memory.id
        taglist = form.tags.data.replace(' ','').replace(';',',').split(',')
        current_app.logger.info(taglist)
        tags_added = 0
        for item in taglist:
            # check if tag already in database
            current_app.logger.info('check if tag {} is already in db'.format(item))
            if Tag.query.filter(Tag.tag==item).first() is None:
                # write to Tag table and remember tag.id
                tag_in = Tag(tag=item)
                db.session.add(tag_in)
                db.session.flush()
                tag_id = tag_in.id       #Tag.query.filter(Tag.tag==item).first()
                current_app.logger.info( 'added new tag {} to db with id {}'.format(item,tag_id) )
            else:
                # get tag.id from db
                tag_id = Tag.query.filter(Tag.tag==item).first().id
                current_app.logger.info( 'old tag {} retrieved from  db with id {}'.format(item,tag_id) )
            # create entry in memory_tag table
            db.session.add(MemoryTag(memory_id=memory_id,tag_id=tag_id))
            db.session.commit()
        return redirect(url_for('memory.index'))
    return render_template('memory/new_memory.html', title='New Memory',form=form)


bp.route('/forgetit', methods=['GET', 'POST'])
@login_required
def forgetit():
     form = ForgetForm()
 
     if form.validate_on_submit():
         current_app.logger.info('keep button return value'.format(form.keep.data)) 
         current_app.logger.info('forget button return value'.format(form.forget.data))
         db.session.commit()
         flash('New memory created!')
         return redirect(url_for('memory.index'))
     return render_template('memory/forget.html', title='Forget or not foget',form=form)
