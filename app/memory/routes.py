# memory

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app, session
from flask_login import current_user, login_required

from wtforms import StringField, SubmitField

from app import db
#from app.main.forms import EditProfileForm, PostForm
from app.memory.forms import NewMemoryForm, EditMemoryForm, ForgetForm, MemoryFilterForm
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
    form = MemoryFilterForm()
    current_app.logger.info('enter memory/index route.')

#    flash("Type " + form.slcType.data)
#    flash("Category " + form.slcCategory.data)

    # if a new session does not have filter settings in place, create else use as is
        
#        flash(session['filter_settings'])
#        flash(session['filter_settings']['type'])

    # work-around for situation where status field does not yet exists
    try:
        if session['filter_settings']:
            pass
    except KeyError:
        current_app.logger.info('No filter settings found in session object: create')
        filter_settings = {}
        filter_settings['status'] = 'off' 
        filter_settings['type'] = 'Any'
        filter_settings['category'] = 'Any'
        filter_settings['tags'] = None
        session['filter_settings'] = filter_settings
        form.filter_status_string = 'Filter is off'


    if not session['filter_settings']:
        current_app.logger.info('No filter settings found in session object: create')
        filter_settings = {}
        filter_settings['status'] = 'off' 
        filter_settings['type'] = 'Any'
        filter_settings['category'] = 'Any'
        filter_settings['tags'] = None
        session['filter_settings'] = filter_settings
        form.filter_status_string = 'Filter is off'
    else:
        filter_settings = session['filter_settings']
        current_app.logger.info('load filter settings from session. status = ' + filter_settings['status'])
    
    # handle the rare case that status is not set
    try:
        if not filter_settings['status']:
            current_app.logger.info('Initialize filter status. set to off')
            filter_settings['status'] = 'off'
            form.filter_status_string = 'Filter is off'
    except (KeyError, UnboundLocalError):
        current_app.logger.info('Initialize filter status. set to off')
        filter_settings['status'] = 'off'
        form.filter_status_string = 'Filter is off'
        filter_settings['type'] = 'Any'
        filter_settings['category'] = 'Any'
        filter_settings['tags'] = None
        
    current_app.logger.info('filter status before post logic  is ' + filter_settings['status'])
    if form.validate_on_submit():
        current_app.logger.info('SUBMIT DETECTED FROM FORM')
#        current_app.logger.info(form.slcType.data)
        # check if toggle button fired

        if form.sbmApply.data:
            current_app.logger.info('Apply filter')
            pass                            # nothing to do filter will be applied and data refreshed according to OnOff setting

        if form.sbmFilterOnOff.data:
            current_app.logger.info('Toggle filter from ' + filter_settings['status'])
            if filter_settings['status']=='on':
                filter_settings['status']='off'
                form.filter_status_string = 'Filter is off'
            else:
                filter_settings['status']='on'
                form.filter_status_string = 'Filter is on'
            current_app.logger.info('after toggle filter at ' + filter_settings['status'])

        if filter_settings['status'] == 'on':
            current_app.logger.info('filter on, settings submitted, update filter_settings on to off. type:' + str(form.slcType.data))
            filter_settings['type'] = form.slcType.data
            filter_settings['category'] = form.slcCategory.data
            filter_settings['tags'] = form.stfTags.data
            session['filter_settings'] = filter_settings
        else:
            current_app.logger.info('filter set to off.default')
            filter_settings['type'] = 'Any'
            filter_settings['category'] = 'Any'
            filter_settings['tags'] = None
        
    elif request.method=='GET':
        current_app.logger.info('request.method is GET.')
        pass
        # if after session expiry session object does not conatin filter_settings

    current_app.logger.info('session filter status is ' + filter_settings['status'])
    if filter_settings['status'] == 'off':
        form.filter_status_string = 'Filter is off'
    else:
        form.filter_status_string = 'Filter is on'

    current_app.logger.info('filter toggle button setting: ' + form.filter_status_string) 

#    form.slcType.default = filter_settings['type']
#    form.slcCategory.default = filter_settings['category']
#    form.stfTags.default = filter_settings['tags']

    page = request.args.get('page', 1, type=int)
    current_app.logger.info('filter_status is ' + filter_settings['status']) 
    if filter_settings['status']=='on':
        current_app.logger.info('Filter is on, get filtered reults')
        memories = current_user.get_filtered_memories(filter_settings).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    else:
        current_app.logger.info('Filter is of, get unfiltered reults')
        memories = current_user.get_memories().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    
    current_app.logger.info('user is: {}'.format(current_user.username))
    current_app.logger.info('output memories: {}'.format(current_user.get_memories()))

    next_url = url_for('memory.index', page=memories.next_num) \
        if memories.has_next else None
    prev_url = url_for('memory.index', page=memories.prev_num) \
        if memories.has_prev else None

    session['filter_settings'] = filter_settings
    return render_template('memory/index.html', title='Memories', form=form,
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
            memory.dormant=True
            db.session.commit()
            flash('Forgotten, that is sad')
            return redirect(url_for('memory.index'))
        elif form.keep.data:
            # keep
            flash('Keep this memory')    
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


@bp.route('/view', methods=['GET'])
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
    
    # get filter settings to create default for type and category field
    # 
    # add attributes from the doc portion of the memories
    # 1. find the type of memory which has to created
    # get type from args
    filter_settings = session['filter_settings']

    memory_type = filter_settings['type'].lower()
    current_app.logger.info('create new memory of type {}'.format(memory_type))

    # 2. get the dictionary with the definition of the various document types. If 'any' set to news as default
    if memory_type == 'any':
        current_app.logger.info('memory type any detected, set to news/Any, update filter settings accordingly')
        memory_type = 'news'
        filter_settings['type'] = 'News'
        filter_settings['category'] = 'Any'
    prescription = current_app.config['DOCUMENTS'][memory_type]
    current_app.logger.info('load memory structure for {}, found {}'.format(memory_type,prescription))

    class TmpMemoryForm(NewMemoryForm):
        pass

    # 3. iterate through the prescription and add fields accordingly [JB: Performance Issues?]
    for item in prescription.keys():
        current_app.logger.info('contains: {}'.format(prescription[item]['key']))
        if prescription.get('field_type') is None:
            setattr(TmpMemoryForm, prescription[item]['key'], StringField(prescription[item]['label']))

    fields = prescription
    #setattr(TmpMemoryForm, 'source', StringField('Source'))
    #setattr(NewMemoryForm, 'source_url', StringField('Source URL'))
    #setattr(TmpMemoryForm, 'submit', SubmitField('Remember this'))

    form = TmpMemoryForm()
    # form.memorize.label.text = "Hallo"

    jsondoc={}
    
    current_app.logger.info('looking for posts: {}'.format(request))
    if (request.method == "POST") & (form.sbmBack.data):
            current_app.logger.info('Back button pressed.')
            return redirect(url_for('memory.index'))

    if (request.method == "POST") & (form.sbmApplyFilter.data):
            session['filter_settings']['type'] = form.slcType.data.lower()
            current_app.logger.info('Apply filter. Set type to {}'.format(session['filter_settings']['type']))
            
            # recreate form
            prescription = current_app.config['DOCUMENTS'][session['filter_settings']['type']]
            class TmpMemoryForm(NewMemoryForm):
                pass
            # iterate through the prescription and add fields accordingly [JB: Performance Issues?]
            for item in prescription.keys():
                current_app.logger.info('contains: {}'.format(prescription[item]['key']))
                if prescription.get('field_type') is None:
                    setattr(TmpMemoryForm, prescription[item]['key'], StringField(prescription[item]['label']))
            fields = prescription

            return render_template('memory/new_memory.html', title='New Memory Type',form=form, fields=fields)

    if form.validate_on_submit():
        if form.sbmMemorize.data:
            current_app.logger.info('New memory posted for create.')
            jsondoc['source'] = form.source.data
            jsondoc['source_url'] = form.source_url.data
            memory = Memory(type=form.slcType.data, 
                            category=form.slcCategory.data,
                            abstract=form.tafAbstract.data,
                            doc=jsondoc,
                            user_id=current_user.id,
                            memorized=datetime.now())
            db.session.add(memory)
            db.session.commit()
            flash('New memory created!')

            # add tags to list
            memory_id = memory.id
            taglist = form.strTags.data.replace(' ','').replace(';',',').split(',')
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
        else:
            pass
    else:
        flash_errors(form)
    return render_template('memory/new_memory.html', title='New Memory',form=form, fields=fields)

"""
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
"""
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
