"use strict";
/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ForceView = exports.ForceModel = void 0;
/* eslint-disable @typescript-eslint/camelcase */
// TODO: Upgrade to newest version of jupyter-widgets/base
const base_1 = require("@jupyter-widgets/base");
const standalone_1 = require("vis-network/standalone");
const types_1 = require("./types");
const version_1 = require("./version");
const feather_icons_1 = __importDefault(require("feather-icons"));
const jquery_1 = __importDefault(require("jquery"));
require("jquery-ui/ui/widgets/draggable");
require("jquery-ui/ui/widgets/resizable");
// Import the CSS
require("../css/widget.css");
feather_icons_1.default.replace();
/*
graph_notebook_widgets is a module to define the front-end modules for our kernel-sid ForceWidget.
It is made up of two classes (ForceModel and ForceView). The ForceModel contains only metadata which also exists on
the browser.

The ForceView is the class used by the browser for rendering. Because it is going to render elements
on the DOM, it extends widget.DOMWidgetView, and must provide an implementation for the class "render"
*/
class ForceModel extends base_1.DOMWidgetModel {
    // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: ForceModel.model_name, _model_module: ForceModel.model_module, _model_module_version: ForceModel.model_module_version, _view_name: ForceModel.view_name, _view_module: ForceModel.view_module, _view_module_version: ForceModel.view_module_version });
    }
}
exports.ForceModel = ForceModel;
ForceModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ForceModel.model_name = "ForceModel";
ForceModel.model_module = version_1.MODULE_NAME;
ForceModel.model_module_version = version_1.MODULE_VERSION;
ForceModel.view_name = "ForceView"; // Set to null if no view
ForceModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ForceModel.view_module_version = version_1.MODULE_VERSION;
class ForceView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.networkDiv = document.createElement("div");
        this.canvasDiv = document.createElement("div");
        this.menu = document.createElement("div");
        this.expandDiv = document.createElement("div");
        this.searchDiv = document.createElement("div");
        this.searchOptionsDiv = document.createElement("div");
        this.resetDiv = document.createElement("div");
        this.detailsDiv = document.createElement("div");
        this.physicsDiv = document.createElement("div");
        this.nodeDataset = new types_1.NodeDataSet(new Array(), {});
        this.edgeDataset = new types_1.EdgeDataSet(new Array(), {});
        this.visOptions = {};
        this.vis = null;
        this.detailsPanel = document.createElement("div");
        this.detailsHeader = document.createElement("div");
        this.graphPropertiesTable = document.createElement("table");
        this.emptyDetailsMessage = document.createElement("p");
        this.graphTableDiv = document.createElement("div");
        this.resizeHandle = document.createElement("div");
        this.detailsContainer = document.createElement("div");
        this.noDataMessage = "No additional data from data source found.";
        this.noElementSelectedMessage = "Select a single node or edge to see more.";
        this.expandBtn = document.createElement("button");
        this.nodeIDSearchMatches = new Array();
        this.edgeIDSearchMatches = new Array();
        this.excludeIDsFromSearch = false;
        this.closeButton = document.createElement("button");
        this.detailsText = document.createElement("p");
        this.searchOptionsBtn = document.createElement("button");
        this.searchMatchColorEdge = "rgba(9,120,209,1)";
        this.searchMatchColorNode = {
            background: "rgba(210, 229, 255, 1)",
            border: "#0978D1",
        };
        this.resetBtn = document.createElement("button");
        this.doingReset = false;
        this.detailsBtn = document.createElement("button");
        this.selectedNodeID = "";
        this.physicsBtn = document.createElement("button");
    }
    render() {
        this.networkDiv.classList.add("network-div");
        this.canvasDiv.style.height = "600px";
        this.canvasDiv.style.width = "100%";
        this.networkDiv.appendChild(this.canvasDiv);
        this.menu.classList.add("menu-div");
        this.networkDiv.appendChild(this.menu);
        this.networkDiv.appendChild(this.detailsPanel);
        /*
        When rendering the ForceView, the widget is given a div to attach everything to which will be added to the
        output section of the cell it was displayed in. This div can be accessed using "this.el"
        */
        this.el.appendChild(this.networkDiv);
        /*
        You can retrieve state from the Kernel's widget model by calling "this.get('trait_name')" which will retrieve the json
        representation of the traitlet that 'trait_name' corresponds to. If the trait is a number or string, only that data will be
        returned, not json.
         */
        const network = this.model.get("network");
        this.visOptions = this.model.get("options");
        this.populateDatasets(network);
        const dataset = {
            nodes: this.nodeDataset,
            edges: this.edgeDataset,
        };
        this.vis = new standalone_1.Network(this.canvasDiv, dataset, this.stripCustomPhysicsOptions());
        setTimeout(() => {
            var _a;
            (_a = this.vis) === null || _a === void 0 ? void 0 : _a.stopSimulation();
        }, this.visOptions.physics.simulationDuration);
        /*
                To listen to messages sent from the kernel, you can register callback methods in the view class,
                this can be done using the "this.listenTo" method.
    
                For our purposes, the first param will always be 'this.model'. The second param is the message name which we
                are subscribing to. For messages triggered by a kernel trait changing its state, the message name will be
                'change:trait_name'. The third param is a reference to the callback function to be invoked when the given
                message occurs. This callback can receive the payload of the message if it would like to. The fourth and final
                parameter is used to keep a way to reference 'this' in the scope of the ForceView class.
                */
        this.listenTo(this.model, "msg:custom", this.interceptCustom);
        this.listenTo(this.model, "change:network", this.changeNetwork);
        this.listenTo(this.model, "change:options", this.changeOptions);
        this.buildActions();
        this.registerVisEvents();
        this.registerWidgetEvents();
    }
    /**
     * Take the json from a given network, and update our datasets
     * used to render the vis Network.
     *
     * @remarks
     * Used at the initial rendering of the force widget, or any time
     * we override the network entirely
     *
     * @param network - The network to update this ForceView's datasets
     */
    populateDatasets(network) {
        const edges = this.linksToEdges(network.graph.links);
        this.nodeDataset.update(network.graph.nodes);
        this.edgeDataset.update(edges);
    }
    /**
     * Triggered when the network traitlet on the Kernel-side is overridden. In this case,
     * the currently rendered network will cleared with the nodes and links present in the new network
     */
    changeNetwork() {
        const network = this.model.get("network");
        this.populateDatasets(network);
    }
    /**
     * Triggered when the options traitlet is overridden on the Kernel-side. This will trigger updating the
     * options of the vis rendering.
     */
    changeOptions() {
        this.visOptions = this.model.get("options");
        if (this.vis == null) {
            return;
        }
        this.vis.setOptions(this.stripCustomPhysicsOptions());
    }
    /**
     * Returns a modified visOptions, with the custom simulationDuration and disablePhysicsAfterInitialSimulation physics
     * options removed. This prevents an error from being thrown when VisJS parses visOptions.
     */
    stripCustomPhysicsOptions() {
        const visOptionsNoCustomPhysics = Object.assign({}, JSON.parse(JSON.stringify(this.visOptions)));
        delete visOptionsNoCustomPhysics["physics"]["simulationDuration"];
        delete visOptionsNoCustomPhysics["physics"]["disablePhysicsAfterInitialSimulation"];
        return visOptionsNoCustomPhysics;
    }
    /**
     * Take custom messages from the kernel and route them to the appropriate handler.
     * Each custom message will have a method field, and a corresponding data field which contains the payload
     * from the message.
     *
     * @remarks
     * NOTE: The method field is only present because all our custom messages build their payloads in this
     * fashion.
     */
    interceptCustom(msg) {
        const msgData = msg["data"];
        switch (msg["method"]) {
            case "add_node":
                this.addNode(msgData);
                break;
            case "add_node_data":
                this.addNodeData(msgData);
                break;
            case "add_node_property":
                this.addNodeProperty(msgData);
                break;
            case "add_edge":
                this.addEdge(msgData);
                break;
            case "add_edge_data":
                this.addEdgeData(msgData);
                break;
            default:
                console.log("unsupported method found", msg["method"]);
        }
    }
    /**
       * Add a node to the nodes dataset, merging the new node with the existing one
       * if this id is already present.
       *
       * The payload coming to this handler from the Kernel will look like:
       {
            "node_id": "1234",
            "data": {
              "label": "SJC",
              "properties": {
                "type": "airport",
                "runways": "4"
              }
            }
          }
       */
    addNode(msgData) {
        if (!msgData.hasOwnProperty("node_id")) {
            // message data must have an id to add a node
            return;
        }
        const id = msgData["node_id"];
        let node = this.nodeDataset.get(id);
        if (node === null) {
            // node with given id was not found...
            // The node does not exist, we can convert this object to one and add it.
            node = types_1.VisNode.fromObject(Object.assign({ id: id }, msgData["data"]));
        }
        else {
            // The node exists, we need to merge the msg data to it and update the dataset
            node = types_1.VisNode.mergeObject(node, msgData["data"]);
        }
        if (!node.hasOwnProperty("label")) {
            // no label found, using node id
            node["label"] = id;
        }
        this.nodeDataset.update([node]);
        return;
    }
    /**
       * Handler to add new data to a node. The input to this is the same as the input to
       * adding a node, because adding a node checks for whether a given id existed,
       * and merges them if the node does.
       *
       * Example input:
       {
            "node_id": "1234",
            "data": {
              "properties": {
                "new_prop": "value"
              }
            }
          }
       */
    addNodeData(msgData) {
        this.addNode(msgData);
    }
    /**
       * Add a key-value pair to a node under its "properties" field
       * If the node does not exist, we will create it with this property.
       * Example input:
  
       {
            "node_id": "1234",
            "key": "foo",
            "value": "bar"
          }
  
       * Example result:
       {
            "node_id": "1234",
            "data": {
              "label": "SJC",
              "properties": {
                "type": "airport",
                "runways": "4",
                "foo": "bar"
              }
            }
          }
       */
    addNodeProperty(msgData) {
        const properties = new types_1.DynamicObject();
        properties[msgData["key"]] = msgData["value"];
        this.addNode({
            node_id: msgData["node_id"],
            data: { properties: properties },
        });
    }
    /**
       * Add an edge to the edgeDataset. Before attempting to add an edge, we will
       * ensure that it has the fields we need to create a VisEdge as they are represented
       * by the add_edge EventfulNetwork method. That payload looks like:
       *
       * @remarks
       * NOTE: we have two different labels here because the top-level "label" is used for displaying,
       * while the inner "properties" label field is the actual value that the underlying structure had.
       * For example, for GremlinNetworks, each edge will have a label, but a user might want to choose the property
       * "code" for us in displaying. In that case, the value of the property "code" would be set to the top-level
       * "label" field.
       {
            "edge_id": "to",
            "from_id": "MKE2DFW",
            "label": "to",
            "to_id": "DFW",
            "data": {
              "label": "to"
            }
       }
       */
    addEdge(msgData) {
        // To be able to add an edge, we require the message to have:
        // 'from_id', 'to_id', and 'edge_id'
        if (!msgData.hasOwnProperty("from_id") ||
            !msgData.hasOwnProperty("to_id") ||
            !msgData.hasOwnProperty("edge_id")) {
            return;
        }
        // check if we have a label. if we do not, use the edge id.
        const label = msgData.hasOwnProperty("label")
            ? msgData["label"]
            : msgData["edge_id"];
        const innerData = msgData.hasOwnProperty("data") ? msgData["data"] : {};
        const edgeID = msgData["from_id"] + ":" + msgData["to_id"] + ":" + msgData["edge_id"];
        // rearrange the data to add to a node to ensure it conforms to the format of a vis-edge.
        // More info found here: https://github.com/visjs/vis-network
        const copiedData = Object.assign({ from: msgData["from_id"], to: msgData["to_id"], id: edgeID, label: label }, innerData);
        let edge = this.edgeDataset.get(edgeID);
        if (edge === null) {
            // edge does not exist, we need to create a new one from this payload
            edge = types_1.VisEdge.fromObject(copiedData);
        }
        else {
            edge = types_1.VisEdge.mergeObject(edge, copiedData);
        }
        this.edgeDataset.update([edge]);
    }
    /**
     * Handler to add more data to an edge. The received payload is identical to
     * that of adding an edge, so we defer to that handler instead.
     */
    addEdgeData(data) {
        this.addEdge(data);
    }
    /**
     * Convert networkx links to Edges. To do this, we want to convert
     * "source" into "from"
     * "target" into "to"
     * and "key" into "id"
     *
     * @remarks
     * This is performed anytime we override the network which is backing this visualization.
     */
    linksToEdges(links) {
        const edges = new Array();
        const propsToSkip = ["source", "target", "key"];
        links.forEach(function (link) {
            const edge = new types_1.VisEdge(link.source, link.target, link.key, link.label);
            // get all other properties on the link and add them to the edge.
            for (const propName in link) {
                if (!(propName in propsToSkip)) {
                    edge[propName] = link[propName];
                }
            }
            edges.push(edge);
        });
        return edges;
    }
    /**
     * Handler to route events observed on the vis network.
     */
    registerVisEvents() {
        var _a, _b, _c, _d, _e, _f, _g;
        (_a = this.vis) === null || _a === void 0 ? void 0 : _a.on("click", (properties) => {
            if (properties.nodes.length === 0 && properties.edges.length === 1) {
                this.handleEdgeClick(properties.edges[0]);
            }
            else if (properties.nodes.length === 0 &&
                properties.edges.length === 0) {
                this.handleEmptyClick();
            }
        });
        (_b = this.vis) === null || _b === void 0 ? void 0 : _b.on("selectNode", (params) => {
            this.handleNodeClick(params.nodes[0]);
        });
        (_c = this.vis) === null || _c === void 0 ? void 0 : _c.on("deselectNode", (params) => {
            console.log("deselect");
            params.previousSelection.nodes.forEach((value) => {
                this.handleDeselectNode(value);
            });
        });
        (_d = this.vis) === null || _d === void 0 ? void 0 : _d.on("dragStart", (params) => {
            const nodeIDs = {};
            params.nodes.forEach((value) => {
                nodeIDs[value] = true;
            });
            if (!nodeIDs.hasOwnProperty(this.selectedNodeID) &&
                params.nodes.length > 0) {
                this.handleDeselectNode(this.selectedNodeID);
            }
            this.handleNodeClick(params.nodes[0]);
        });
        (_e = this.vis) === null || _e === void 0 ? void 0 : _e.on("startStabilizing", () => {
            setTimeout(() => {
                var _a;
                (_a = this.vis) === null || _a === void 0 ? void 0 : _a.stopSimulation();
            }, this.visOptions.physics.simulationDuration);
        });
        (_f = this.vis) === null || _f === void 0 ? void 0 : _f.on("selectEdge", (params) => {
            params.edges.forEach((value) => {
                this.handleEdgeClick(params.edges[0]);
            });
        });
        (_g = this.vis) === null || _g === void 0 ? void 0 : _g.on("stabilized", () => {
            var _a;
            if (this.visOptions.physics.disablePhysicsAfterInitialSimulation == true) {
                this.visOptions.physics.enabled = false;
                this.changeOptions();
            }
            if (this.doingReset) {
                (_a = this.vis) === null || _a === void 0 ? void 0 : _a.fit({
                    animation: true,
                });
                this.doingReset = false;
            }
        });
    }
    /**
     * handle deselecting any number of nodes, ensuring the a node which was selected and is a current valid
     * search match does not recieve the wrong border color indicating a search match.
     * @param nodeID
     */
    handleDeselectNode(nodeID) {
        var _a;
        console.log("handle deselect");
        const node = this.nodeDataset.get(nodeID);
        if (node === null) {
            return;
        }
        if (nodeID !== undefined && nodeID !== null && node.id === nodeID) {
            if (!node.group) {
                node.color = this.searchMatchColorNode;
                node.font = { color: "black" };
            }
        }
        else {
            node.color = this.visOptions.nodes.color;
        }
        node.borderWidth = 0;
        this.nodeDataset.update(node);
        (_a = this.vis) === null || _a === void 0 ? void 0 : _a.stopSimulation();
        this.selectedNodeID = "";
    }
    /**
     * When an empty click is detected, the details panel needs to be cleared to show the appropriate message
     */
    handleEmptyClick() {
        this.hideGraphProperties();
        this.detailsText.innerText = "Details";
        this.setDetailsMessage(this.noElementSelectedMessage);
    }
    /**
     * Hide the generated table of graph properties and show an empty message
     */
    hideGraphProperties() {
        if (this.emptyDetailsMessage.classList.contains("displayNone")) {
            this.emptyDetailsMessage.classList.toggle("displayNone");
        }
        if (!this.graphTableDiv.classList.contains("displayNone")) {
            this.graphTableDiv.classList.toggle("displayNone");
        }
    }
    /**
     * Build the Properties section of the details panel from a given node or edge.
     *
     * @param data - a node or edge
     */
    buildGraphPropertiesTable(data) {
        const graphTable = jquery_1.default(this.graphPropertiesTable);
        let rows;
        if (data.hasOwnProperty("properties")) {
            rows = this.buildTableRows(data.properties);
            jquery_1.default(graphTable).empty();
            jquery_1.default(graphTable).append(...rows);
            this.showGraphProperties();
        }
        else {
            this.hideGraphProperties();
            this.setDetailsMessage(this.noDataMessage);
        }
    }
    /**
     * ensure that the table containing graph properties is visible, and that the empty
     * message advising the user to select a node or edge is hidden
     */
    showGraphProperties() {
        if (this.graphTableDiv.classList.contains("displayNone")) {
            this.graphTableDiv.classList.toggle("displayNone");
        }
        if (!this.emptyDetailsMessage.classList.contains("displayNone")) {
            this.emptyDetailsMessage.classList.toggle("displayNone");
        }
    }
    setDetailsMessage(message) {
        jquery_1.default(this.emptyDetailsMessage).text(message);
    }
    /**
     * Take an arbitrary object and convert its kvps into tr elements
     * with two columns. The first column is the key, the second is the value.
     *
     * @param data - a dictionary to turn into rows of a table
     */
    buildTableRows(data) {
        const rows = new Array();
        const sorted = Object.entries(data).sort((a, b) => {
            return a[0].localeCompare(b[0]);
        });
        sorted.forEach((entry) => {
            const row = document.createElement("tr");
            const property = document.createElement("td");
            const value = document.createElement("td");
            property.appendChild(document.createTextNode(entry[0].toString()));
            value.appendChild(document.createTextNode(entry[1].toString()));
            row.appendChild(property);
            row.appendChild(value);
            rows.push(row);
        });
        if (rows.length === 0) {
            const row = document.createElement("tr");
            const td = document.createElement("td");
            td.appendChild(document.createTextNode("No additional data from data source found."));
            row.appendChild(td);
            rows.push(row);
        }
        return rows;
    }
    /**
     * Handle a single node being clicked. This will build details tables for all
     * key-value pairs which are on the edge. all key-value pairs which appear under the
     * "properties" top-level key will be treated as data which exists on the graph which
     * was queried to gather this data. All others are treated as data which is used by vis.
     *
     * @param nodeID - the id of the edge as represented by this.vis
     */
    handleNodeClick(nodeID) {
        var _a;
        if (nodeID === undefined) {
            return;
        }
        this.handleDeselectNode(this.selectedNodeID);
        const node = this.nodeDataset.get(nodeID);
        if (node === null) {
            return;
        }
        if (node.label !== undefined && node.label !== "") {
            this.detailsText.innerText = "Details - " + node.title;
        }
        else {
            this.detailsText.innerText = "Details";
        }
        this.buildGraphPropertiesTable(node);
        if (node.group) {
            node.font = { bold: true };
            node.opacity = 1;
            node.borderWidth = 3;
        }
        else {
            node.font = { color: "white" };
        }
        this.nodeDataset.update(node);
        (_a = this.vis) === null || _a === void 0 ? void 0 : _a.stopSimulation();
        this.selectedNodeID = nodeID;
    }
    /**
     * Handle a single edge being clicked. This will build details tables for all
     * key-value pairs which are on the edge. all key-value pairs which appear under the
     * "properties" top-level key will be treated as data which exists on the graph which
     * was queried to gather this data. All others are treated as data which is used by vis.
     *
     * @param edgeID - the id of the edge as represented by this.vis
     */
    handleEdgeClick(edgeID) {
        const edge = this.edgeDataset.get(edgeID);
        if (edge === null) {
            return;
        }
        if (edge.title !== undefined && edge.title !== "") {
            this.detailsText.innerText = "Details - " + edge.title;
        }
        else {
            this.detailsText.innerText = "Details";
        }
        this.buildGraphPropertiesTable(edge);
    }
    /**
     * Searches for the provided text under all nodes and edges in this.vis
     * If any property or key contains the text, that edge or node will be highlighted
     *
     * NOTE: Case sensitive.
     * @param text - The content to search for
     */
    handleSearchInput(text) {
        var _a, _b, _c, _d, _e;
        const nodeUpdate = [];
        const edgeUpdate = [];
        const nodeIDs = {};
        const edgeIDs = {};
        const selectedNodes = {};
        (_a = this.vis) === null || _a === void 0 ? void 0 : _a.getSelectedNodes().forEach((nodeID) => {
            selectedNodes[nodeID] = true;
        });
        const selectedEdges = {};
        (_b = this.vis) === null || _b === void 0 ? void 0 : _b.getSelectedEdges().forEach((edgeID) => {
            selectedEdges[edgeID] = true;
        });
        if (text !== "") {
            // all matched nodes should be colors a light blue
            this.nodeDataset.forEach((item, id) => {
                const searchFound = this.search(text, item, 0, this.excludeIDsFromSearch);
                if (searchFound) {
                    const nodeID = id.toString();
                    nodeUpdate.push({
                        id: nodeID,
                        borderWidth: 3,
                    });
                    nodeIDs[id.toString()] = true;
                }
            });
            // all matched edges should be colored a light blue
            this.edgeDataset.forEach((item, id) => {
                const searchFound = this.search(text, item, 0, this.excludeIDsFromSearch);
                if (searchFound) {
                    edgeUpdate.push({
                        id: id.toString(),
                        width: 3,
                        color: this.searchMatchColorEdge,
                    });
                    edgeIDs[id.toString()] = true;
                }
            });
        }
        else {
            //Reset the opacity and border width
            this.nodeDataset.forEach((item, id) => {
                const nodeID = id.toString();
                nodeUpdate.push({
                    id: nodeID,
                    opacity: 1,
                    borderWidth: 0,
                });
                nodeIDs[id.toString()] = true;
            });
        }
        // check current matched nodes and clear all nodes which are no longer matches
        this.nodeIDSearchMatches.forEach((value) => {
            if (nodeIDs.hasOwnProperty(value.toString())) {
                return;
            }
            else {
                const selected = selectedNodes.hasOwnProperty(value.toString());
                nodeUpdate.push({
                    id: value.toString(),
                    borderWidth: selected
                        ? this.visOptions["nodes"]["borderWidthSelected"]
                        : 0,
                    opacity: 0.35,
                });
            }
        });
        // check current matched edges and clear all nodes which are no longer matches
        this.edgeIDSearchMatches.forEach((value) => {
            if (edgeIDs.hasOwnProperty(value.toString())) {
                return;
            }
            else {
                edgeUpdate.push({
                    id: value.toString(),
                    width: 1,
                    color: this.visOptions["edges"]["color"],
                });
            }
        });
        // check if physics have been manually disabled/enabled, set flag to indicate that this setting shouldn't be changed
        let re_enable_physics = false;
        if (this.visOptions.physics.enabled == true) {
            (_c = this.vis) === null || _c === void 0 ? void 0 : _c.setOptions({ physics: false });
            re_enable_physics = true;
        }
        this.nodeDataset.update(nodeUpdate);
        this.edgeDataset.update(edgeUpdate);
        if (re_enable_physics) {
            (_d = this.vis) === null || _d === void 0 ? void 0 : _d.setOptions({ physics: true });
            (_e = this.vis) === null || _e === void 0 ? void 0 : _e.stopSimulation();
        }
        this.nodeIDSearchMatches = Object.keys(nodeIDs);
        this.edgeIDSearchMatches = Object.keys(edgeIDs);
    }
    /**
     * Builds the side panel of actions and any other elements that they rely on.
     * Currently, this includes action icons for Search, Details, and Maximize
     * as well as a panel which is revealed when the details action is toggled.
     * This extra panel will show the details of a given selected node.
     */
    buildActions() {
        const rightActions = document.createElement("div");
        rightActions.classList.add("right-actions");
        this.menu.append(rightActions);
        this.expandDiv.classList.add("menu-action", "expand-div");
        this.searchDiv.classList.add("menu-action", "search-div");
        this.searchOptionsDiv.classList.add("menu-action", "search-options-div");
        this.resetDiv.classList.add("menu-action", "reset-div");
        this.detailsDiv.classList.add("menu-action", "details-div");
        this.physicsDiv.classList.add("menu-action", "physics-div");
        this.searchOptionsBtn.title = "Exclude/Include UUIDs in Search";
        this.searchOptionsBtn.innerHTML = feather_icons_1.default.icons["user-check"].toSvg();
        this.searchOptionsDiv.appendChild(this.searchOptionsBtn);
        rightActions.append(this.searchOptionsDiv);
        this.searchOptionsBtn.onclick = () => {
            this.excludeIDsFromSearch = !this.excludeIDsFromSearch;
            if (this.excludeIDsFromSearch) {
                this.searchOptionsBtn.innerHTML = feather_icons_1.default.icons["user-x"].toSvg();
            }
            else {
                this.searchOptionsBtn.innerHTML = feather_icons_1.default.icons["user-check"].toSvg();
            }
        };
        const searchInput = document.createElement("input");
        searchInput.classList.add("search-bar");
        searchInput.type = "search";
        searchInput.placeholder = "search";
        searchInput.onkeyup = () => {
            this.handleSearchInput(searchInput.value);
        };
        this.searchDiv.append(searchInput);
        rightActions.append(this.searchDiv);
        this.resetBtn.title = "Reset Graph View";
        this.resetBtn.innerHTML = feather_icons_1.default.icons["refresh-cw"].toSvg();
        this.resetDiv.appendChild(this.resetBtn);
        rightActions.append(this.resetDiv);
        this.resetBtn.onclick = () => {
            this.visOptions.physics.enabled = true;
            this.changeOptions();
            this.physicsBtn.innerHTML = feather_icons_1.default.icons["unlock"].toSvg();
            this.doingReset = true;
        };
        this.physicsBtn.title = "Enable/Disable Graph Physics";
        if (this.visOptions.physics.enabled == true &&
            this.visOptions.physics.disablePhysicsAfterInitialSimulation == false) {
            this.physicsBtn.innerHTML = feather_icons_1.default.icons["unlock"].toSvg();
        }
        else {
            this.physicsBtn.innerHTML = feather_icons_1.default.icons["lock"].toSvg();
        }
        this.physicsDiv.appendChild(this.physicsBtn);
        rightActions.append(this.physicsDiv);
        this.physicsBtn.onclick = () => {
            this.visOptions.physics.disablePhysicsAfterInitialSimulation = false;
            this.visOptions.physics.enabled = !this.visOptions.physics.enabled;
            this.changeOptions();
            if (this.visOptions.physics.enabled == true) {
                this.physicsBtn.innerHTML = feather_icons_1.default.icons["unlock"].toSvg();
            }
            else {
                this.physicsBtn.innerHTML = feather_icons_1.default.icons["lock"].toSvg();
            }
        };
        this.detailsBtn.innerHTML = feather_icons_1.default.icons["list"].toSvg();
        this.detailsBtn.title = "Details";
        this.detailsDiv.appendChild(this.detailsBtn);
        rightActions.append(this.detailsDiv);
        this.detailsBtn.onclick = () => {
            this.handleDetailsToggle();
        };
        this.closeButton.onclick = () => {
            this.handleDetailsToggle();
        };
        //build the div which the details button toggles
        this.detailsContainer.classList.add("details-container");
        this.detailsPanel.classList.add("details", "hidden");
        this.detailsPanel.style.top = "100px";
        this.detailsPanel.style.left = "100px";
        this.detailsHeader.classList.add("details-header");
        this.detailsText.className = "details-text";
        this.closeButton.className = "close-button";
        this.detailsHeader.append(this.detailsText, this.closeButton);
        this.closeButton.innerText = "x";
        this.detailsText.innerText = "Details";
        const detailsFooter = document.createElement("div");
        detailsFooter.classList.add("details-footer");
        const detailsFooterButton = document.createElement("button");
        detailsFooterButton.classList.add("details-footer-button");
        detailsFooterButton.textContent = "Close";
        detailsFooter.append(detailsFooterButton);
        detailsFooterButton.onclick = () => {
            this.handleDetailsToggle();
        };
        this.detailsPanel.appendChild(this.detailsContainer);
        this.graphPropertiesTable.classList.add("properties-table");
        this.graphTableDiv.classList.add("properties-content", "displayNone");
        this.graphTableDiv.append(this.graphPropertiesTable);
        this.emptyDetailsMessage.textContent =
            "Select a single node or edge to see more.";
        this.emptyDetailsMessage.classList.add("emptyDetails");
        this.resizeHandle.classList.add("resizeHandle");
        this.detailsContainer.append(this.detailsHeader, this.emptyDetailsMessage, this.graphTableDiv, detailsFooter);
        this.expandBtn.innerHTML = feather_icons_1.default.icons["maximize-2"].toSvg();
        this.expandBtn.title = "Fullscreen";
        this.expandBtn.onclick = () => {
            this.toggleExpand();
        };
        this.expandDiv.appendChild(this.expandBtn);
        rightActions.append(this.expandDiv);
        const dragOptions = new types_1.ForceDraggableOptions();
        dragOptions.handle = ".details-header";
        dragOptions.containment = "parent";
        jquery_1.default(this.detailsPanel).draggable(dragOptions);
        const resizeOptions = new types_1.ForceResizableOptions();
        resizeOptions.handles = "s, e, w, se, sw";
        resizeOptions.resize = (event, ui) => {
            this.detailsContainer.style.height = ui.size.height.toString() + "px";
            this.detailsContainer.style.width = ui.size.width.toString() + "px";
        };
        jquery_1.default(this.detailsPanel).resizable(resizeOptions);
        const zoomInDiv = document.createElement("div");
        const zoomOutDiv = document.createElement("div");
        const zoomResetDiv = document.createElement("div");
        const zoomInButton = document.createElement("button");
        zoomInButton.title = "Zoom In";
        zoomInButton.onclick = () => {
            var _a, _b;
            (_a = this.vis) === null || _a === void 0 ? void 0 : _a.moveTo({
                scale: ((_b = this.vis) === null || _b === void 0 ? void 0 : _b.getScale()) * 2,
                animation: true,
            });
        };
        const zoomOutButton = document.createElement("button");
        zoomOutButton.title = "Zoom Out";
        zoomOutButton.onclick = () => {
            var _a, _b;
            (_a = this.vis) === null || _a === void 0 ? void 0 : _a.moveTo({
                scale: ((_b = this.vis) === null || _b === void 0 ? void 0 : _b.getScale()) * 0.5,
                animation: true,
            });
        };
        const zoomResetButton = document.createElement("button");
        zoomResetButton.title = "Reset Zoom to Fit";
        zoomResetButton.onclick = () => {
            var _a;
            (_a = this.vis) === null || _a === void 0 ? void 0 : _a.fit({
                animation: true,
            });
        };
        zoomInButton.innerHTML = feather_icons_1.default.icons["zoom-in"].toSvg();
        zoomOutButton.innerHTML = feather_icons_1.default.icons["zoom-out"].toSvg();
        zoomResetButton.innerHTML = feather_icons_1.default.icons["square"].toSvg();
        zoomInDiv.classList.add("menu-action", "zoom-in-div");
        zoomOutDiv.classList.add("menu-action", "zoom-out-div");
        zoomResetDiv.classList.add("menu-action", "zoom-reset-div");
        zoomInDiv.append(zoomInButton);
        zoomOutDiv.append(zoomOutButton);
        zoomResetDiv.append(zoomResetButton);
        const bottomRightActions = document.createElement("div");
        bottomRightActions.classList.add("bottom-right");
        bottomRightActions.append(zoomInDiv, zoomResetDiv, zoomOutDiv);
        this.networkDiv.append(bottomRightActions);
    }
    handleDetailsToggle() {
        this.detailsBtn.classList.toggle("active");
        this.detailsPanel.classList.toggle("hidden");
    }
    /**
     * Search the provided data for an instance of the given text
     * @param text - the search term
     * @param data - data to be searched
     * @param excludeIDs - boolean indicating whether we want to highlight ID matches
     */
    search(text, data, depth, excludeIDs) {
        if (Array.isArray(data)) {
            for (let i = 0; i < data.length; i++) {
                if (this.search(text, data[i], depth + 1, excludeIDs)) {
                    return true;
                }
            }
            return false;
        }
        else if (typeof data === "object") {
            let found = false;
            // an object can be null
            if (data === null || data === undefined) {
                return found;
            }
            Object.entries(data).forEach((entry) => {
                if (found) {
                    return true;
                }
                // we want to ignore the top level set of properties on an object except for "properties"
                // because otherwise we would search for vis-specific settings.
                if (depth === 0) {
                    // Also include top level label, in case of label by ID
                    if (["properties", "label"].includes(entry[0].toString())) {
                        found = this.search(text, entry[1], depth + 1, excludeIDs);
                    }
                    else {
                        console.log("Not properties or label key, ignoring.");
                    }
                }
                else {
                    if (!(this.excludeIDsFromSearch &&
                        [
                            "~id",
                            "~start",
                            "~end",
                            "T.id",
                            "Direction.IN",
                            "Direction.OUT",
                        ].includes(entry[0].toString()))) {
                        found = this.search(text, entry, depth + 1, excludeIDs);
                    }
                    else {
                        console.log("entry[0] is ID property, skipping.");
                    }
                }
            });
            return found;
        }
        else if (data === null || data === undefined) {
            return false;
        }
        else {
            // If recursion reached variable not a map or array, check it.
            return data.toString().indexOf(text) !== -1;
        }
    }
    /**
     * Take this widget to full screen mode, ensuring that the positioning of the details
     * panel remains in the same relative position that it was in before full screen mode.
     */
    toggleExpand() {
        const elem = this.networkDiv;
        const doc_fullScreenElement_multibrowser = document;
        const elem_requestFullscreen_multibrowser = document.documentElement;
        const doc_exitFullscreen_multibrowser = document;
        const fullScreenElement_multibrowser = doc_fullScreenElement_multibrowser.fullscreenElement ||
            doc_fullScreenElement_multibrowser.webkitFullscreenElement ||
            doc_fullScreenElement_multibrowser.mozFullScreenElement ||
            doc_fullScreenElement_multibrowser.msFullscreenElement;
        const requestFullscreen_multibrowser = elem_requestFullscreen_multibrowser.requestFullscreen ||
            elem_requestFullscreen_multibrowser.mozRequestFullScreen ||
            elem_requestFullscreen_multibrowser.webkitRequestFullscreen ||
            elem_requestFullscreen_multibrowser.msRequestFullscreen;
        const exitFullscreen_multibrowser = doc_exitFullscreen_multibrowser.exitFullscreen ||
            doc_exitFullscreen_multibrowser.webkitExitFullscreen ||
            doc_exitFullscreen_multibrowser.msExitFullscreen ||
            doc_exitFullscreen_multibrowser.mozCancelFullScreen;
        const fullscreenchange = (event) => {
            const detailsTop = parseInt(this.detailsPanel.style.top);
            const detailsLeft = parseInt(this.detailsPanel.style.left);
            if (fullScreenElement_multibrowser) {
                this.detailsPanel.style.left =
                    (detailsLeft / 650) * window.innerWidth + "px";
                this.detailsPanel.style.top =
                    (detailsTop / 650) * window.innerHeight + "px";
                this.expandBtn.innerHTML = feather_icons_1.default.icons["minimize-2"].toSvg();
                this.expandBtn.title = "Exit Fullscreen";
            }
            else {
                this.detailsPanel.style.left =
                    (detailsLeft / window.innerWidth) * 650 + "px";
                const top = (detailsTop / window.innerHeight) * 650;
                const newTop = this.detailsPanel.offsetHeight + top < 650
                    ? top
                    : top - this.detailsPanel.offsetHeight;
                this.detailsPanel.style.top = newTop + "px";
                console.log(newTop);
                this.expandBtn.innerHTML = feather_icons_1.default.icons["maximize-2"].toSvg();
                this.expandBtn.title = "Fullscreen";
                document.removeEventListener("fullscreenchange", fullscreenchange);
            }
            this.expandBtn.classList.toggle("active");
        };
        if (!fullScreenElement_multibrowser) {
            if (requestFullscreen_multibrowser) {
                document.addEventListener("fullscreenchange", fullscreenchange);
                requestFullscreen_multibrowser.call(elem);
                this.canvasDiv.style.height = "100%";
            }
        }
        else {
            if (exitFullscreen_multibrowser) {
                exitFullscreen_multibrowser.call(document);
                this.canvasDiv.style.height = "600px";
            }
        }
        return;
    }
    /**
     * Register any needed events to this.el, the containing element for this widget
     */
    registerWidgetEvents() {
        /*
        Use the MutationObserver to find when this widget is first given width. Once this event is seen,
        fit the vis network onto the canvas and then disconnect the observer so that it is not done again.
        This will prevent the graph from being rendered in such a way that the user cannot see it if
        the initial state of the widget is hidden.
         */
        const observerConfig = {
            attributes: true,
            childList: false,
            subtree: true,
        };
        let observer;
        const observerCallback = (mutationsList, observer) => {
            var _a;
            for (const mutation of mutationsList) {
                if (mutation.type === "attributes") {
                    if (mutation.attributeName === "width" &&
                        mutation.oldValue === null &&
                        mutation.target[mutation.attributeName] !== null &&
                        mutation.target[mutation.attributeName] !== undefined &&
                        mutation.target[mutation.attributeName] > 0) {
                        (_a = this.vis) === null || _a === void 0 ? void 0 : _a.fit();
                        observer.disconnect();
                    }
                }
            }
        };
        // eslint-disable-next-line prefer-const
        observer = new MutationObserver(observerCallback);
        observer.observe(this.el, observerConfig);
    }
}
exports.ForceView = ForceView;
