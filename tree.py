import os
 
from tkinter import *
from tkinter import ttk     #@Reimport
from All_Item import *
 
# from demopanels import MsgPanel, SeeDismissPanel
 
# Constants for formatting file sizes
KB = 1024.0
MB = KB * KB
GB = MB * KB
 
class TreeDemo(ttk.Frame):
     
    def __init__(self, isapp=True, name='treedemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Tree Demo')
        self.isapp = isapp
        self._create_widgets()
         
    def _create_widgets(self):
        self._create_demo_panel()
         
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
         
        self._create_treeview(demoPanel)   
        self._populate_root()
                     
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
        self.tree.bind('<<TreeviewOpen>>', self._update_tree)
         
    def _populate_root(self):
        self.yhcraw = YhCraw()
        self.root_list = self.yhcraw.get_yahoo_title()

        self.root_parent = list()
        for title in self.root_list:
          name = title['name']
          link = title['link']
          self.tree.insert('', END, text=name , values=[link], tags = 'title')

    def _populate_tree(self, parent_node, result_list, tag):
      for content in result_list:
        name = content['name']
        link = content['link']
        self.tree.insert(parent_node, END, text=name, values=[link], tags = tag)

    def _update_tree(self, event): #@UnusedVariable
        # user expanded a node - build the related directory
        nodeId     = self.tree.focus()      # the id of the expanded node
        node_dict  = self.tree.item(nodeId)
        link       = node_dict['values'][0]
        parent_tag = node_dict['tags'][0]
        print(parent_tag)
        input("p")

        if (parent_tag == "title"):
          self.stitle_list = self.yhcraw.get_yahoo_sub_title(link)
          self._populate_tree(nodeId, self.stitle_list, "stitle")
        elif (parent_tag == "stitle"):
          self.cate_list = self.yhcraw.get_yahoo_category(link)
          self._populate_tree(nodeId, self.cate_list, "category")
        elif (parent_tag == "category"):
          self.item_list = self.yhcraw.get_yahoo_item(link)
          self._populate_tree(nodeId, self.item_list, "item")
        else:
          return

 
if __name__ == '__main__':
    TreeDemo().mainloop()
