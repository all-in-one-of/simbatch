from lib.common import CommonFunctions
from io import *

# JSON Name Format, PEP8 Name Format
PROJECT_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'project_name'),
    ('stateId', 'state_id'),
    ('state', 'state'),
    ('isDefault', 'is_default'),
    ('dirProj', 'project_directory'),
    ('dirWrk', 'working_directory'),
    ('dirCam', 'cameras_directory'),
    ('dirCach', 'cache_directory'),
    ('dirEnv', 'env_directory'),
    ('dirProp', 'props_directory'),
    ('dirScr', 'scripts_directory'),
    ('dirCust', 'custom_directory'),
    ('pattern', 'seq_shot_take_pattern'),
    ('zerosInVersion', 'zeros_in_version'),
    ('desc', 'description')]


class SingleProject:
    DEF_STATE_FOR_NEW_PROJ = "ACTIVE"
    DEF_STATE_ID_FOR_NEW_PROJ = 22
    comfun = None

    def __init__(self, project_id, project_name, is_default, state_id, state, project_directory, working_directory,
                 cameras_directory, cache_directory, env_directory, props_directory, scripts_directory,
                 custom_directory, seq_shot_take_pattern, description, zeros_in_version=3):
        self.comfun = CommonFunctions()

        self.id = project_id
        self.project_name = project_name
        self.project_directory = self.comfun.get_proper_path(project_directory, info="proj dir")
        self.working_directory = self.comfun.get_proper_path(working_directory, info="wrk dir")
        self.cameras_directory = self.comfun.get_proper_path(cameras_directory, info="cam dir")
        self.cache_directory = self.comfun.get_proper_path(cache_directory, info="ani cache dir")
        self.env_directory = self.comfun.get_proper_path(env_directory, info="env dir")
        self.props_directory = self.comfun.get_proper_path(props_directory, info="props dir")
        self.scripts_directory = self.comfun.get_proper_path(scripts_directory, info="scripts dir")
        self.custom_directory = self.comfun.get_proper_path(custom_directory, info="custom dir")

        self.working_directory_absolute = ""
        self.cameras_directory_absolute = ""
        self.cache_directory_absolute = ""
        self.env_directory_absolute = ""
        self.props_directory_absolute = ""
        self.scripts_directory_absolute = ""
        self.custom_directory_absolute = ""
        # self.frame_range_directory_absolute = self.working_directory_absolute + "\\frame_range\\"  # TODO frame range
        self.is_default = is_default
        if state_id == 0:
            state_id = self.DEF_STATE_ID_FOR_NEW_PROJ
            state = self.DEF_STATE_FOR_NEW_PROJ
        self.state_id = state_id
        self.state = state
        self.seq_shot_take_pattern = seq_shot_take_pattern
        self.zeros_in_version = zeros_in_version
        self.description = description
        self.update_absolute_directories()

    def update_absolute_directories(self):
        if self.comfun.is_absolute(self.working_directory) is False:
            self.working_directory_absolute = self.project_directory + self.working_directory
        else:
            self.working_directory_absolute = self.working_directory
        if self.comfun.is_absolute(self.cameras_directory) is False:
            self.cameras_directory_absolute = self.project_directory + self.cameras_directory
        else:
            self.cameras_directory_absolute = self.cameras_directory
        if self.comfun.is_absolute(self.cache_directory) is False:
            self.cache_directory_absolute = self.project_directory + self.cache_directory
        else:
            self.cache_directory_absolute = self.cache_directory
        if self.comfun.is_absolute(self.env_directory) is False:
            self.env_directory_absolute = self.project_directory + self.env_directory
        else:
            self.env_directory_absolute = self.env_directory
        if self.comfun.is_absolute(self.props_directory) is False:
            self.props_directory_absolute = self.project_directory + self.props_directory
        else:
            self.props_directory_absolute = self.props_directory
        if self.comfun.is_absolute(self.scripts_directory) is False:
            self.scripts_directory_absolute = self.project_directory + self.scripts_directory
        else:
            self.scripts_directory_absolute = self.scripts_directory
        if self.comfun.is_absolute(self.custom_directory) is False:
            self.custom_directory_absolute = self.project_directory + self.custom_directory
        else:
            self.custom_directory_absolute = self.custom_directory


class Projects:
    batch = None
    comfun = None

    projects_data = []
    current_project = None
    current_project_index = None
    current_project_id = None
    max_id = 0
    total_projects = 0

    sample_data_checksum = None
    sample_data_total = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.sts = batch.sts
        self.debug_level = batch.sts.debug_level
        self.projects_data = []

    def __repr__(self):
        return "Projects(SimBatch())"

    def __str__(self):
        return "current_project_id:{}   total_projects:{}".format(self.current_project_id, self.total_projects)

    #  print project data, for debug
    def print_current(self):
        print "     current project: id: {}     index: {}    total_projects: {}\n".format(self.current_project_id,
                                                                                          self.current_project_index,
                                                                                          self.total_projects)
        if self.current_project_index is not None:
            cur_proj = self.current_project
            print "       current project: ", cur_proj.project_name
            print "       project_directory ", cur_proj.project_directory
            print "       working_directory ", cur_proj.working_directory
            print "       cameras_directory ", cur_proj.cameras_directory
            print "       cache_directory ", cur_proj.cache_directory
            print "       seq_shot_take_pattern:{}, zeros:{}, description:{}".format(cur_proj.seq_shot_take_pattern,
                                                                                     cur_proj.zeros_in_version,
                                                                                     cur_proj.description)

    def print_all(self):
        if self.total_projects == 0:
            print "   [INF] no projects loaded"
        for p in self.projects_data:
            print "\n\n   {} id:{} is_default:{} state:{}".format(p.project_name, p.id, p.is_default, p.state)
            print "   ", p.project_directory,
            print "   ", p.working_directory_absolute
            print "   seq_shot_take_pattern:{}, zeros:{}, description:{}".format(p.seq_shot_take_pattern,
                                                                                 p.zeros_in_version,
                                                                                 p.description)
        print "\n\n"

    #  get index from list 'projects_data'  by id of project
    def get_index_from_id(self, id):
        for i, p in enumerate(self.projects_data):
            if p.id == id:
                return i
        return None

    #  get index from name for form copy schema
    def get_id_from_name(self, name, check_similar=False):
        for p in self.projects_data:
            if name == p.project_name:
                return p.id
        if check_similar:
            for p in self.projects_data:
                if name.lower() in p.project_name.lower():
                    return p.id
        return None

    #  update id, index and current for fast use by all modules
    def update_current_from_id(self, proj_id):
        if proj_id is None:
            self.current_project_id = self.get_default_project_id()
        else:
            self.current_project_id = proj_id
        self.current_project_index = self.get_index_from_id(self.current_project_id)
        if self.current_project_index is not None:
            self.current_project = self.projects_data[self.current_project_index]
            return True
        else:
            self.batch.logger.err("(update_current_from_id)  no index found:{}".format(proj_id))
            self.current_project_id = None
            return False

    #  update id, index and current for fast use by all modules
    def update_current_from_index(self, index):
        if 0 <= index < self.total_projects:
            self.current_project_index = index
            self.current_project_id = self.projects_data[index].id
            self.current_project = self.projects_data[index]
            return True
        else:
            self.current_project_id = None
            self.current_project = None
            self.batch.logger.err(("(update_current_from_index) wrong index:", index))
            self.batch.logger.err(" total:{}  len:{}".format(self.total_projects, len(self.projects_data)))
            return False

    #  prepare 'projects_data' for backup or save
    def format_projects_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.batch.logger.err("(format_projects_data) no format param !")
        else:
            if json or backup:
                t = self.comfun.get_current_time()
                json_data = {"projects": {"meta": {"total": self.total_projects,
                                                   "timestamp": t,
                                                   "jsonFormat": "http://json-schema.org/"},
                                          "data": {}}}
                for i, p in enumerate(self.projects_data):
                    proj = {}
                    for field in PROJECT_ITEM_FIELDS_NAMES:
                        proj[field[0]] = eval('p.'+field[1])
                        json_data["projects"]["data"][i] = proj
                return json_data
            else:
                # PRO version with SQL
                self.batch.logger.inf("PRO version with SQL")
                return False

    def create_project(self, project_id, project_name, is_default, state_id, state, project_directory, working_directory,
                 cameras_directory, cache_directory, env_directory, props_directory, scripts_directory,
                 custom_directory, seq_shot_take_pattern, description, zeros_in_version=3):
        return SingleProject(project_id, project_name, is_default, state_id, state, project_directory, working_directory,
                 cameras_directory, cache_directory, env_directory, props_directory, scripts_directory,
                 custom_directory, seq_shot_take_pattern, description, zeros_in_version=zeros_in_version)

    #  add project to 'projects_data' list  on load  and on add by user
    def add_project(self, project_to_add, do_save=False, generate_directory_patterns=False):
        if project_to_add.id > 0:
            self.max_id = project_to_add.id
        else:
            self.max_id += 1
            project_to_add.id = self.max_id

        if self.max_id == 1:
            project_to_add.is_default = 1

        #  generate_directory_patterns for current project
        #  pattern is generated basis on directories structure on storage
        #  used for construct new path, generate path for load
        if generate_directory_patterns:
            project_to_add.seq_shot_take_pattern = self.batch.sio.get_dir_patterns(project_to_add.cache_directory)

        self.projects_data.append(project_to_add)
        self.total_projects += 1
        if project_to_add.is_default == 1:
            self.set_proj_as_default(id=project_to_add.id)
        if do_save:
            self.save_projects()
        return project_to_add.id

    def update_project(self, mock_project, do_save=False):   # "mock_project" used for transfer data from ui
        if self.current_project_index is not None:
            up_proj = self.projects_data[self.current_project_index]
            up_proj.project_name = mock_project.project_name
            up_proj.project_directory = mock_project.project_directory
            up_proj.working_directory = mock_project.working_directory
            up_proj.cameras_directory = mock_project.cameras_directory
            up_proj.cache_directory = mock_project.cache_directory
            if mock_project.is_default == 1 and up_proj.is_default == 0:
                up_proj.is_default = mock_project.is_default
                self.set_proj_as_default(index=self.current_project_index)
            up_proj.description = mock_project.description
            if do_save is True:
                self.save_projects()
        else:
            self.batch.logger.err("(update_project) self.current_project_index is None")

    #  check is project with index is default
    def check_is_default(self, index=None):
        if index is not None:
            if self.projects_data[index].is_default == 1:
                return True
            else:
                return False
        else:
            return False

    #  search all project for default
    def get_default_project_id(self):
        for p in self.projects_data:
            if p.is_default == 1:
                return p.id
        return None

    #  set def project init after loading
    def set_proj_as_default(self, id=-1, index=-1):
        if index >= 0:
            for p in self.projects_data:
                if p.is_default == 1:
                    p.is_default = 0
            self.projects_data[index].is_default = 1
            return True
        elif id >= 0:
            for p in self.projects_data:
                if p.id == id:
                    p.is_default = 1
                else:
                    if p.is_default == 1:
                        p.is_default = 0
            return True
        else:
            return False

    #  set def val after loading
    def init_default_proj(self):
        if len(self.projects_data) > 0:
            for i, p in enumerate(self.projects_data):
                if p.is_default == 1:
                    self.current_project_index = i
            self.update_current_from_index(self.current_project_index)
        else:
            self.current_project_index = None

    #  clear 'projects_data' list  on refresh, before reload
    def clear_all_projects_data(self, clear_stored_data=False):
        del self.projects_data[:]
        self.max_id = 0
        self.total_projects = 0
        self.current_project_id = None
        self.current_project_index = None
        if clear_stored_data:
            if self.sts.store_data_mode == 1:
                if self.clear_json_project_file():
                    return True
                else:
                    return False
            if self.sts.store_data_mode == 2:
                if self.clear_projects_in_mysql():
                    return True
                else:
                    return False
        return True

    #  example data for beginner users and for tests
    def create_example_project_data(self, do_save=True):
        collect_ids = 0
        sample_project_1 = SingleProject(0, "Sample Proj 1", 1, 0, "defState", "C:\\exampleProj\\", "exampleWokingDir",
                                         "cam", "cache", "env", "props", "scripts", "custom",
                                         "<seq##>\<seq##>_<sh###>", "sample project 1")
        sample_project_2 = SingleProject(0, "Sample Proj 2", 1, 0, "defState", "D:\\proj\\", "fx",
                                         "cam", "cache", "env", "props", "scripts", "custom",
                                         "<seq##>\\<sh###>", "sample project 2")
        sample_project_3 = SingleProject(0, "Sample Proj 3", 1, 0, "defState", "E:\\exampleProj\\", "exampleWokingDir",
                                         "cam", "cache", "env", "props", "scripts", "custom",
                                         "s_<sh##>", "sample project 3")
        collect_ids += self.add_project(sample_project_1)
        collect_ids += self.add_project(sample_project_2)
        collect_ids += self.add_project(sample_project_3, do_save=do_save)
        self.sample_data_checksum = 6
        self.sample_data_total = 3
        return collect_ids

    #  load projects data after startup or after reload
    def load_projects(self):
        if self.sts.store_data_mode == 1:
            return self.load_projects_from_json()
        if self.sts.store_data_mode == 2:
            return self.load_projects_from_mysql()

    #  load projects data form json
    def load_projects_from_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_PROJECTS_FILE_NAME
        if self.comfun.file_exists(json_file, info="projects file"):
            self.batch.logger.inf(("loading projects: ", json_file))
            json_projects = self.comfun.load_json_file(json_file)
            if json_projects is not None and "projects" in json_projects.keys():
                if json_projects['projects']['meta']['total'] > 0:
                    for li in json_projects['projects']['data'].values():
                        if len(li) == len(PROJECT_ITEM_FIELDS_NAMES):
                            new_project = SingleProject(int(li['id']), li['name'], int(li['isDefault']),
                                                        int(li['stateId']), li['state'], li['dirProj'], li['dirWrk'],
                                                        li['dirCam'], li['dirCach'], li['dirEnv'], li['dirProp'],
                                                        li['dirScr'], li['dirCust'], li['pattern'], li['desc'],
                                                        li['zerosInVersion'])
                            self.add_project(new_project)
                        else:
                            self.batch.logger.err(("proj data not consistent", len(li), len(PROJECT_ITEM_FIELDS_NAMES)))
                    return True
            else:
                self.batch.logger.wrn(("no projects data in : ", json_file))
                return False
        else:
            self.batch.logger.wrn(("projects file not exists : ", json_file))
            return False

    #  load projects data from sql
    def load_projects_from_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    #  save projects
    def save_projects(self):
        if self.sts.store_data_mode == 1:
            return self.save_projects_to_json()
        if self.sts.store_data_mode == 2:
            return self.save_projects_to_mysql()

    #  save projects data as json
    def save_projects_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_PROJECTS_FILE_NAME
        content = self.format_projects_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    #  save projects data to sql
    def save_projects_to_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    #  remove single project
    def remove_single_project(self, index=None, id=None, do_save=False):
        if index is None and id is None:
            return False
        if id > 0:
            for i, q in enumerate(self.projects_data):
                if q.id == id:
                    del self.projects_data[i]
                    self.total_projects -= 1
                    break
            if do_save is False:
                return True
        if index >= 0:
            del self.projects_data[index]
            self.total_projects -= 1
            if do_save is False:
                return True
        if do_save is True:
            return self.save_projects()

    #  delete json file from storage
    def delete_json_project_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_PROJECTS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
        else:
            return True

    #  clear json file content
    def clear_json_project_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_PROJECTS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return self.comfun.save_to_file(json_file, "")
        else:
            return True

    #  clear project data from sql
    def clear_projects_in_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return True
