"use strict";
(self["webpackChunk_g2nb_nbtools"] = self["webpackChunk_g2nb_nbtools"] || []).push([["lib_plugin_js"],{

/***/ "./lib/databank.js":
/*!*************************!*\
  !*** ./lib/databank.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataBrowser: () => (/* binding */ DataBrowser),
/* harmony export */   Databank: () => (/* binding */ Databank)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _toolbox__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./toolbox */ "./lib/toolbox.js");




class DataBrowser extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.search = null;
        this.databank = null;
        this.addClass('nbtools-data-browser');
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout();
        this.search = new _toolbox__WEBPACK_IMPORTED_MODULE_3__.SearchBox('#nbtools-data-browser > .nbtools-databank');
        this.databank = new Databank(this.search);
        this.layout.addWidget(this.search);
        this.layout.addWidget(this.databank);
    }
}
class Databank extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(associated_search) {
        super();
        this.last_update = 0;
        this.update_waiting = false;
        this.search = associated_search;
        this.addClass('nbtools-databank');
        this.addClass('nbtools-wrapper');
        // Update the databank when the data registry changes
        _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.data_registry.on_update(() => {
            // If the last update was more than 3 seconds ago, update the databank
            if (this.update_stale())
                this.fill_databank();
            else
                this.queue_update(); // Otherwise, queue an update if not already waiting for one
        });
        // Fill the databank with the registered data
        this.fill_databank();
    }
    update_stale() {
        return this.last_update + (3 * 1000) < Date.now();
    }
    queue_update() {
        // If no update is waiting, queue an update
        if (!this.update_waiting) {
            setTimeout(() => {
                this.fill_databank(); // Fill the databank
                this.update_waiting = false; // And mark as no update queued
            }, Math.abs(this.last_update + (3 * 1000) - Date.now())); // Queue for 3 seconds since last update
            this.update_waiting = true; // And mark as queued
        }
    }
    fill_databank() {
        this.last_update = Date.now();
        // Gather collapsed origins and groups
        const collapsed_origins = Array.from(this.node.querySelectorAll('header.nbtools-origin > span.nbtools-collapsed'))
            .map((n) => { var _a; return (_a = n.parentElement) === null || _a === void 0 ? void 0 : _a.getAttribute('title'); });
        const collapsed_groups = Array.from(this.node.querySelectorAll('div.nbtools-group > span.nbtools-collapsed'))
            .map((n) => { var _a, _b; return `${(_a = n.closest('ul.nbtools-origin')) === null || _a === void 0 ? void 0 : _a.getAttribute('title')}||${(_b = n.parentElement) === null || _b === void 0 ? void 0 : _b.getAttribute('title')}`; });
        // First empty the databank
        this.empty_databank();
        // Get the list of data
        const data = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.data_registry.list();
        // Organize by origin and sort
        const origins = Object.keys(data);
        origins.sort((a, b) => {
            const a_name = a.toLowerCase();
            const b_name = b.toLowerCase();
            return (a_name < b_name) ? -1 : (a_name > b_name) ? 1 : 0;
        });
        // Add each origin
        origins.forEach((origin) => {
            const origin_box = this.add_origin(origin);
            if (collapsed_origins.includes(origin))
                this.toggle_collapse(origin_box); // Retain collapsed origins
            const groups = this.origin_groups(data[origin]);
            Object.keys(groups).reverse().forEach((key) => {
                this.add_group(origin_box, key, collapsed_groups.includes(`${origin}||${key}`), groups[key].reverse());
            });
        });
        // Apply search filter after refresh
        this.search.filter(this.search.node.querySelector('input.nbtools-search'));
    }
    origin_groups(origin) {
        const organized = {};
        // Organize data by group
        Object.keys(origin).forEach((uri) => {
            const data = origin[uri][0];
            if (data.group in organized)
                organized[data.group].push(data); // Add data to group
            else
                organized[data.group] = [data]; // Lazily create group
        });
        // Return the organized set of groups
        return organized;
    }
    empty_databank() {
        this.node.innerHTML = '';
    }
    add_origin(name) {
        // Create the HTML DOM element
        const origin_wrapper = document.createElement('div');
        origin_wrapper.innerHTML = `
            <header class="nbtools-origin" title="${name}">
                <span class="nbtools-expanded nbtools-collapse jp-Icon jp-Icon-16 jp-ToolbarButtonComponent-icon"></span>
                ${name}
            </header>
            <ul class="nbtools-origin" title="${name}"></ul>`;
        // Attach the expand / collapse functionality
        const collapse = origin_wrapper.querySelector('span.nbtools-collapse');
        collapse.addEventListener("click", () => this.toggle_collapse(origin_wrapper));
        // Add to the databank
        this.node.append(origin_wrapper);
        return origin_wrapper;
    }
    add_group(origin, group_name, collapsed, group_data) {
        const list = origin.querySelector('ul');
        if (!list)
            return;
        const group_wrapper = document.createElement('li');
        group_wrapper.classList.add('nbtools-tool');
        group_wrapper.setAttribute('title', 'Click to add to notebook');
        group_wrapper.innerHTML = `
            <div class="nbtools-add">+</div>
            <div class="nbtools-header nbtools-group" title="${group_name}">
                <span class="nbtools-expanded nbtools-collapse jp-Icon jp-Icon-16 jp-ToolbarButtonComponent-icon"></span>
                ${group_name}
            </div>
            <ul class="nbtools-group"></ul>`;
        if (collapsed)
            this.toggle_collapse(group_wrapper); // Retain collapsed groups
        for (const data of group_data)
            this.add_data(group_wrapper, data);
        // Attach the expand / collapse functionality
        const collapse = group_wrapper.querySelector('span.nbtools-collapse');
        collapse.addEventListener("click", (event) => {
            this.toggle_collapse(group_wrapper);
            event.stopPropagation();
            return false;
        });
        list.append(group_wrapper);
        // Add the click event
        group_wrapper.addEventListener("click", () => {
            Databank.add_group_cell(list.getAttribute('title'), group_name, group_data);
        });
        return group_wrapper;
    }
    add_data(origin, data) {
        const group_wrapper = origin.querySelector('ul.nbtools-group');
        if (!group_wrapper)
            return;
        const data_wrapper = document.createElement('a');
        data_wrapper.setAttribute('href', data.uri);
        data_wrapper.setAttribute('title', 'Drag to add parameter or cell');
        data_wrapper.classList.add('nbtools-data');
        data_wrapper.innerHTML = `<i class="${data.icon ? data.icon : 'far fa-bookmark'}"></i> ${data.label}`;
        group_wrapper.append(data_wrapper);
        // Add the click event
        data_wrapper.addEventListener("click", event => {
            if (data.widget)
                Databank.add_data_cell(data.origin, data.uri);
            event.preventDefault();
            event.stopPropagation();
            return false;
        });
        // Add the drag event
        data_wrapper.addEventListener("dragstart", event => {
            event.dataTransfer.setData("text/plain", data.uri);
        });
    }
    static add_data_cell(origin, data_uri) {
        // Check to see if nbtools needs to be imported
        const import_line = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.needs_import() ? 'import nbtools\n\n' : '';
        // Add and run a code cell with the generated tool code
        _toolbox__WEBPACK_IMPORTED_MODULE_3__.Toolbox.add_code_cell(import_line + `nbtools.data(origin='${(0,_utils__WEBPACK_IMPORTED_MODULE_1__.escape_quotes)(origin)}', uri='${(0,_utils__WEBPACK_IMPORTED_MODULE_1__.escape_quotes)(data_uri)}')`);
    }
    static add_group_cell(origin, group_name, group_data) {
        // Check to see if nbtools needs to be imported
        const import_line = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.needs_import() ? 'import nbtools\n\n' : '';
        // Add and run a code cell with the generated tool code
        const files = group_data.map((d) => `'${d.uri}'`).join(", ");
        _toolbox__WEBPACK_IMPORTED_MODULE_3__.Toolbox.add_code_cell(import_line + `nbtools.data(origin='${(0,_utils__WEBPACK_IMPORTED_MODULE_1__.escape_quotes)(origin)}', group='${(0,_utils__WEBPACK_IMPORTED_MODULE_1__.escape_quotes)(group_name)}', uris=[${files}])`);
    }
    // TODO: Move to utils.ts and refactor so both this and toolbox.ts calls the function?
    toggle_collapse(origin_wrapper) {
        const list = origin_wrapper.querySelector("ul.nbtools-origin, ul.nbtools-group");
        const collapsed = list.classList.contains('nbtools-hidden');
        // Toggle the collapse button
        const collapse = origin_wrapper.querySelector('span.nbtools-collapse');
        if (collapsed) {
            collapse.classList.add('nbtools-expanded');
            collapse.classList.remove('nbtools-collapsed');
        }
        else {
            collapse.classList.remove('nbtools-expanded');
            collapse.classList.add('nbtools-collapsed');
        }
        // Hide or show widget body
        (0,_utils__WEBPACK_IMPORTED_MODULE_1__.toggle)(list);
    }
}


/***/ }),

/***/ "./lib/dataregistry.js":
/*!*****************************!*\
  !*** ./lib/dataregistry.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Data: () => (/* binding */ Data),
/* harmony export */   DataRegistry: () => (/* binding */ DataRegistry),
/* harmony export */   IDataRegistry: () => (/* binding */ IDataRegistry)
/* harmony export */ });
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");



const IDataRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token("nbtools:IDataRegistry");
class DataRegistry {
    // { 'kernel_id': { 'origin': { 'identifier': data } } }
    /**
     * Initialize the DataRegistry and connect event handlers
     */
    constructor() {
        this.current = null; // Reference to the currently selected notebook or other widget
        this.update_callbacks = []; // Callbacks to execute when the cache is updated
        this.kernel_data_cache = {}; // Keep a cache of kernels to registered data
        // Lazily assign the data registry to the context
        if (!_context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.data_registry)
            _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.data_registry = this;
        _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.context().notebook_focus((current_widget) => {
            // Current notebook hasn't changed, no need to do anything, return
            if (this.current === current_widget)
                return;
            // Otherwise, update the current notebook reference
            this.current = current_widget;
        });
    }
    /**
     * Register all data objects in the provided list
     *
     * @param data_list
     */
    register_all(data_list) {
        let all_good = true;
        for (const data of data_list) {
            data.skip_callbacks = true;
            all_good = this.register(data) && all_good;
        }
        this.execute_callbacks();
        return all_good;
    }
    /**
     * Register data for the sent to/come from menus
     * Return whether registration was successful or not
     *
     * @param origin
     * @param uri
     * @param label
     * @param kind
     * @param group
     * @param icon
     * @param data
     * @param widget
     * @param skip_callbacks
     */
    register({ origin = null, uri = null, label = null, kind = null, group = null, icon = null, data = null, widget = false, skip_callbacks = false }) {
        // Use origin, identifier, label and kind to initialize data, if needed
        if (!data)
            data = new Data(origin, uri, label, kind, group, widget, icon);
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return false; // If no kernel, do nothing
        // Lazily initialize dict for kernel cache
        let cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            cache = this.kernel_data_cache[kernel_id] = {};
        // Lazily initialize dict for origin
        let origin_data = cache[data.origin];
        if (!origin_data)
            origin_data = cache[data.origin] = {};
        // Add to cache, execute callbacks and return
        if (!origin_data[data.uri])
            origin_data[data.uri] = [];
        origin_data[data.uri].unshift(data);
        if (!skip_callbacks)
            this.execute_callbacks();
        return true;
    }
    /**
     * Unregister data with the given origin and identifier
     * Return the unregistered data object
     * Return null if un-registration was unsuccessful
     *
     * @param origin
     * @param identifier
     * @param data
     */
    unregister({ origin = null, uri = null, data = null }) {
        // Use origin, identifier and kind to initialize data, if needed
        if (!data)
            data = new Data(origin, uri);
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return null; // If no kernel, do nothing
        // If unable to retrieve cache, return null
        const cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            return null;
        // If unable to retrieve origin, return null
        const origin_data = cache[data.origin];
        if (!origin_data)
            return null;
        // If unable to find identifier, return null;
        let found = origin_data[data.uri];
        if (!found || !found.length)
            return null;
        // Remove from the registry, execute callbacks and return
        found = origin_data[data.uri].shift();
        if (!origin_data[data.uri].length)
            delete origin_data[data.uri];
        this.execute_callbacks();
        return found;
    }
    /**
     * Execute all registered update callbacks
     */
    execute_callbacks() {
        for (const c of this.update_callbacks)
            c();
    }
    /**
     * Attach a callback that gets executed every time the data in the registry is updated
     *
     * @param callback
     */
    on_update(callback) {
        this.update_callbacks.push(callback);
    }
    /**
     * Update the data cache for the current kernel
     *
     * @param message
     */
    update_data(message) {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return; // Do nothing if no kernel
        // Parse the message
        const data_list = message['data'];
        // Update the cache
        this.kernel_data_cache[kernel_id] = {};
        this.register_all(data_list);
    }
    /**
     * List all data currently in the registry
     */
    list() {
        // If no kernel, return empty map
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return {};
        // If unable to retrieve cache, return empty map
        const cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            return {};
        // FORMAT: { 'origin': { 'identifier': [data] } }
        return cache;
    }
    /**
     * Get all data that matches one of the specified kinds or origins
     * If kinds or origins is null or empty, accept all kinds or origins, respectively
     *
     * @param kinds
     * @param origins
     */
    get_data({ kinds = null, origins = null }) {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return {}; // If no kernel, return empty
        // If unable to retrieve cache, return empty
        const cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            return {};
        // Compile map of data with a matching origin and kind
        const matching = {};
        for (let origin of Object.keys(cache)) {
            if (origins === null || origins.length === 0 || origins.includes(origin)) {
                const hits = {};
                for (let data of Object.values(cache[origin])) {
                    if (data[0].kind === 'error')
                        continue;
                    if (kinds === null || kinds.length === 0 || kinds.includes(data[0].kind))
                        hits[data[0].label] = data[0].uri;
                }
                if (Object.keys(hits).length > 0)
                    matching[origin] = hits;
            }
        }
        return matching;
    }
    /**
     * Retrieve the kernel ID from the currently selected notebook
     * Return null if no kernel or no notebook selected
     */
    current_kernel_id() {
        return _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.context().kernel_id(this.current);
    }
}
class Data {
    constructor(origin, uri, label = null, kind = null, group = null, widget = false, icon = null) {
        this.origin = origin;
        this.uri = uri;
        this.label = !!label ? label : (0,_utils__WEBPACK_IMPORTED_MODULE_2__.extract_file_name)(uri);
        this.kind = !!kind ? kind : (0,_utils__WEBPACK_IMPORTED_MODULE_2__.extract_file_type)(uri);
        this.group = group;
        this.widget = widget;
        this.icon = icon;
    }
}


/***/ }),

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _basewidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./basewidget */ "./lib/basewidget.js");
/* harmony import */ var _uioutput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./uioutput */ "./lib/uioutput.js");
/* harmony import */ var _uibuilder__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./uibuilder */ "./lib/uibuilder.js");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _toolbox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./toolbox */ "./lib/toolbox.js");
/* harmony import */ var _databank__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./databank */ "./lib/databank.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./registry */ "./lib/registry.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _dataregistry__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./dataregistry */ "./lib/dataregistry.js");















const module_exports = Object.assign(Object.assign(Object.assign({}, _basewidget__WEBPACK_IMPORTED_MODULE_3__), _uioutput__WEBPACK_IMPORTED_MODULE_4__), _uibuilder__WEBPACK_IMPORTED_MODULE_5__);
const EXTENSION_ID = '@g2nb/nbtools:plugin';
const NAMESPACE = 'nbtools';
/**
 * The nbtools plugin.
 */
const nbtools_plugin = {
    id: EXTENSION_ID,
    provides: [_registry__WEBPACK_IMPORTED_MODULE_9__.IToolRegistry, _dataregistry__WEBPACK_IMPORTED_MODULE_14__.IDataRegistry],
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_11__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_11__.ILabShell, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_12__.INotebookTracker],
    activate: activate_widget_extension,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (nbtools_plugin);
/**
 * Activate the widget extension.
 */
async function activate_widget_extension(app, widget_registry, settings, mainmenu, restorer, shell, notebook_tracker) {
    // Initialize the ContextManager
    init_context(app, notebook_tracker);
    // Initialize settings
    const setting_dict = await init_settings(settings);
    // Create the tool and data registries
    const tool_registry = new _registry__WEBPACK_IMPORTED_MODULE_9__.ToolRegistry(setting_dict);
    const data_registry = new _dataregistry__WEBPACK_IMPORTED_MODULE_14__.DataRegistry();
    // Add items to the help menu
    add_help_links(app, mainmenu);
    // Add keyboard shortcuts
    add_keyboard_shortcuts(app, tool_registry);
    // Add the toolbox
    add_tool_browser(app, restorer);
    // Add the databank
    add_data_browser(app, restorer);
    // Register the nbtools widgets with the widget registry
    widget_registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION,
        exports: module_exports,
    });
    // Register the plugin as loaded
    (0,_utils__WEBPACK_IMPORTED_MODULE_10__.usage_tracker)('labextension_load', location.protocol + '//' + location.host + location.pathname);
    // Return the tool registry so that it is provided to other extensions
    return [tool_registry, data_registry];
}
async function init_settings(settings) {
    let setting = null;
    try {
        setting = await settings.load(EXTENSION_ID);
    }
    catch (_a) {
        console.log('Unable to load nbtools settings');
    }
    return { force_render: setting ? setting.get('force_render').composite : true };
}
function init_context(app, notebook_tracker) {
    _context__WEBPACK_IMPORTED_MODULE_13__.ContextManager.jupyter_app = app;
    _context__WEBPACK_IMPORTED_MODULE_13__.ContextManager.notebook_tracker = notebook_tracker;
    _context__WEBPACK_IMPORTED_MODULE_13__.ContextManager.context();
    window.ContextManager = _context__WEBPACK_IMPORTED_MODULE_13__.ContextManager; // Left in for development purposes
}
function add_keyboard_shortcuts(app, tool_registry) {
    app.commands.addCommand("nbtools:insert-tool", {
        label: 'Insert Notebook Tool',
        execute: () => {
            // Open the tool manager, if necessary
            app.shell.activateById('nbtools-browser');
            (0,_utils__WEBPACK_IMPORTED_MODULE_10__.pulse_red)(document.getElementById('nbtools-browser'));
            // If only one tool is available, add it
            const tools = tool_registry.list();
            if (tools.length === 1)
                _toolbox__WEBPACK_IMPORTED_MODULE_7__.Toolbox.add_tool_cell(tools[0]);
            // Otherwise give the search box focus
            else
                document.querySelector('.nbtools-search').focus();
        },
    });
}
function add_data_browser(app, restorer) {
    const data_browser = new _databank__WEBPACK_IMPORTED_MODULE_8__.DataBrowser();
    data_browser.title.iconClass = 'nbtools-icon fas fa-database jp-SideBar-tabIcon';
    data_browser.title.caption = 'Databank';
    data_browser.id = 'nbtools-data-browser';
    // Add the data browser widget to the application restorer
    if (restorer)
        restorer.add(data_browser, NAMESPACE);
    app.shell.add(data_browser, 'left', { rank: 103 });
}
function add_tool_browser(app, restorer) {
    const tool_browser = new _toolbox__WEBPACK_IMPORTED_MODULE_7__.ToolBrowser();
    tool_browser.title.iconClass = 'nbtools-icon fa fa-th jp-SideBar-tabIcon';
    tool_browser.title.caption = 'Toolbox';
    tool_browser.id = 'nbtools-browser';
    // Add the tool browser widget to the application restorer
    if (restorer)
        restorer.add(tool_browser, NAMESPACE);
    app.shell.add(tool_browser, 'left', { rank: 102 });
}
/**
 * Add the nbtools documentation and feedback links to the help menu
 *
 * @param {Application<Widget>} app
 * @param {IMainMenu} mainmenu
 */
function add_help_links(app, mainmenu) {
    const feedback = 'nbtools:feedback';
    const documentation = 'nbtools:documentation';
    // Add feedback command to the command palette
    app.commands.addCommand(feedback, {
        label: 'g2nb Help Forum',
        caption: 'Open the g2nb help forum',
        isEnabled: () => !!app.shell,
        execute: () => {
            const url = 'https://community.mesirovlab.org/c/g2nb/';
            let element = document.createElement('a');
            element.href = url;
            element.target = '_blank';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
    });
    // Add documentation command to the command palette
    app.commands.addCommand(documentation, {
        label: 'nbtools Documentation',
        caption: 'Open documentation for nbtools',
        isEnabled: () => !!app.shell,
        execute: () => {
            const url = 'https://github.com/g2nb/nbtools#nbtools';
            let element = document.createElement('a');
            element.href = url;
            element.target = '_blank';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
    });
    // Add documentation link to the help menu
    if (mainmenu)
        mainmenu.helpMenu.addGroup([{ command: feedback }, { command: documentation }], 2);
}


/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.3d6a69190252a9993d8d.js.map