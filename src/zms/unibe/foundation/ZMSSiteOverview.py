import json
import xmltodict
import logging
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter, DictExporter

from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo

print("Addon: zms.unibe.foundation.ZMSSiteOverview")
security = ModuleSecurityInfo("zms.unibe.foundation.ZMSSiteOverview")  # allow module import in RestrictedPython

LOGGER = logging.getLogger("ZMSSiteOverview")


class ZMSSiteOverview(ObjectManager):
    security = ClassSecurityInfo()  # control access to class methods in RestrictedPython

    def __init__(self, context, lang="ger"):
        
        self.sites_objs = {}
        self.sites_dict = {}
        self.sites_path = []
        self.tree_nodes = {}
        self.tree_root = None
        
        sites_in_zmsindex = context.zcatalog_index({"meta_id": "ZMS", "path": "/unibe"})
        
        for site in sites_in_zmsindex:
            # TODO: filter out inactive by attribute or context/breadcrumb
            try:
                self.sites_objs[site.getPath()] = site.getObject()
                self.sites_path.append(site.getPath())
            except:
                LOGGER.error(f"Error processing site: {site.get_uid} {site.getPath()}")
                pass

        for path, site in self.sites_objs.items():
            # TODO: introduce headless.REQUEST.set("lang", lang)
            # TODO: to handle ZMSSite.PrimaryLanguage = eng etc. correctly
            if not site.isActive({"lang": lang}):
                continue
            site_xml_dict = xmltodict.parse(site.toXml(
                REQUEST={"lang": lang},
                deep=False,
                data2hex=False,
                multilang=False,
            ))
            attributes = site_xml_dict["ZMS"]
            attributes["protocol"] = site.getConfProperty("ASP.protocol", "http")
            attributes["domain"] = site.getConfProperty("ASP.ip_or_domain")
            attributes["server"] = site.getConfProperty("UniBE.Server")
            attributes["aliases"] = site.getConfProperty("UniBE.Alias")
            attributes["comments"] = site.getConfProperty("UniBE.Comment")
            attributes["robots"] = site.getConfProperty("UniBE.Robots")
            attributes["etracker"] = site.getConfProperty("eTracker-Testaccount")
            attributes["workflow"] = not site.getAutocommit()
            attributes["workflow_nodes"] = site.operator_getattr(site.getWorkflowManager(), "nodes")
            attributes["path"] = path
            attributes["breadcrumbs"] = " > ".join([breadcrumb.getTitle({"lang":lang})
                                                    for breadcrumb in site.breadcrumbs_obj_path()])
            self.sites_dict[path] = attributes
        
        # self.create_tree()
        
    def create_tree(self):

        paths = [x.split("/content") for x in self.sites_path]
        paths.sort()
        
        for path in paths:
            key = path[0]
            value = key.split("/")
            value = list(filter(lambda x: x != "", value))

            if len(value) == 1:  # /unibe
                self.tree_nodes[key] = self.tree_root = Node(value[0])
            elif len(value) > 1:  # /unibe/.../...
                parent_key = "/"+"/".join(value[:-1])
                self.tree_nodes[key] = Node(name=value[-1],
                                            parent=self.tree_nodes[parent_key],
                                            path=key,
                                            #obj=self.sites_objs[key+"/content"],
                                            dict=self.sites_dict[key+"/content"],
                                            )
    @security.public
    def get_sites(self):
        
        return json.dumps([sites for sites in self.sites_dict.values()],
                          indent=4, sort_keys=False)

    @security.public
    def render_tree(self):
        
        print(RenderTree(self.tree_root).by_attr("name"))

    @security.public
    def get_tree_json(self):

        tree = JsonExporter(indent=4, sort_keys=False, ensure_ascii=False)
        return tree.export(self.tree_root)

    @security.public
    def get_tree_dict(self):

        tree = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k != "name###"])
        return tree.export(self.tree_root)


# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(ZMSSiteOverview)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
