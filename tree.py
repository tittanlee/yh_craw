import os
 
from tkinter import *
from tkinter import ttk     #@Reimport
from All_Item import *
 
class TreeDemo(ttk.Frame):
     
  def __init__(self):
    ttk.Frame.__init__(self)
    self.pack(expand=Y, fill=BOTH)
    self.master.title('Yahoo')
    self._create_widgets()

         
  def _create_widgets(self):
    self._create_demo_panel()
       
  def _create_demo_panel(self):
    demoPanel = Frame(self)
    demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
    self._create_treeview(demoPanel)   
    self._populate_root()
    
    self.collect_btn = Button(self, text="Update", command = self._update_sel_items).pack(side = LEFT, fill = X)

  def _create_treeview(self, parent):
    f = ttk.Frame(parent)
    f.pack(side=TOP, fill=BOTH, expand=Y)

    # create the tree and scrollbars
    self.dataCols = ('fullpath', 'type', 'size')       
    self.tree = ttk.Treeview(columns=self.dataCols,
                             displaycolumns='size')

    ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tree.yview)
    xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tree.xview)
    self.tree['yscroll'] = ysb.set
    self.tree['xscroll'] = xsb.set

    # setup column headings
    self.tree.heading('#0', text='', anchor=W)
    self.tree.heading('size', text='', anchor=W)
    self.tree.column('size', stretch=0, width=70)

    # add tree and scrollbars to frame
    self.tree.grid(in_=f, row=0, column=0, sticky=NSEW)
    ysb.grid(in_=f, row=0, column=1, sticky=NS)
    xsb.grid(in_=f, row=1, column=0, sticky=EW)

    # set frame resizing priorities
    f.rowconfigure(0, weight=1)
    f.columnconfigure(0, weight=1)

    # action to perform when a node is expanded
    self.tree.bind('<<TreeviewOpen>>', self._update_tree_by_toggle)

  def _populate_root(self):
    self.yhcraw = YhCraw()
    self.root_list = self.yhcraw.get_yahoo_title()

    self.root_parent = list()
    for title in self.root_list:
      name = title['name']
      link = title['link']
      root_node_id = self.tree.insert('', END, text=name , values=[link], tags = 'title')
      self.root_parent.append(root_node_id)

  def _update_sel_items(self):
    select_item_list = self.tree.selection()
    for sel_item in select_item_list:
      node_dict = self.tree.item(sel_item)
      name       = node_dict['text']
      link       = node_dict['values'][0]
      parent_tag = node_dict['tags'][0]

      child_list = self.tree.get_children(sel_item)
      if child_list:
        continue 

      self._update_tree(sel_item, recursive = True)



  def _populate_tree(self, parent_node, result_list, tag):
    new_node_id_list = list()
    for content in result_list:
      name = content['name']
      link = content['link']
      new_node_id = self.tree.insert(parent_node, END, text=name, values=[link], tags = tag)
      new_node_id_list.append(new_node_id)

    return new_node_id_list

  def _update_tree_by_toggle(self, event): 
    nodeId     = self.tree.focus()

    child_list = self.tree.get_children(nodeId)
    if child_list:
      return
    self._update_tree(nodeId, recursive = False)

  def _update_tree(self, nodeId, recursive = False):
    node_dict  = self.tree.item(nodeId)
    name       = node_dict['text']
    link       = node_dict['values'][0]
    parent_tag = node_dict['tags'][0]
    new_node_id = None

    if (parent_tag == "title"):
      self.stitle_list = self.yhcraw.get_yahoo_sub_title(link)
      id_list = self._populate_tree(nodeId, self.stitle_list, "stitle")
    elif (parent_tag == "stitle"):
      self.cate_list = self.yhcraw.get_yahoo_category(link)
      id_list = self._populate_tree(nodeId, self.cate_list, "category")
    elif (parent_tag == "category"):
      self.item_list = self.yhcraw.get_yahoo_item(link)
      id_list = self._populate_tree(nodeId, self.item_list, "item")
    else:
      print("%s %s" %(name, link))
      return

    if recursive == True:
      for new_node_id in id_list:
        print("new_node_id = %s" %new_node_id)
        self._update_tree(new_node_id, recursive)








if __name__ == '__main__':
  TreeDemo().mainloop()
