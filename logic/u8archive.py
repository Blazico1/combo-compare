import struct
import oead
import os

class Node:
    def __init__(self, node_type, name_offset, data_offset_or_parent_index, size_or_next_node_index):
        self.node_type = node_type
        self.name_offset = name_offset
        self.data_offset_or_parent_index = data_offset_or_parent_index
        self.size_or_next_node_index = size_or_next_node_index
        self.name = None  # This will be set later

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return (f"Node(type={'Directory' if self.node_type == 1 else 'File'}, "
                f"string_offset=0x{self.name_offset:X}, "
                f"name={self.name}, "
                f"data_offset_or_parent_index=0x{self.data_offset_or_parent_index:X}, "
                f"size_or_next_node_index=0x{self.size_or_next_node_index:X})")

class U8Archive:
    def __init__(self, path):
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            raise ValueError(f"File {path} not found")
        
        self.data = self._decompress_data(data)
        self.header = self._parse_header()
        self.nodes = self._parse_nodes()
        self._parse_file_names()

    def _decompress_data(self, data):
        if data[:4] == b'Yaz0':
            return oead.yaz0.decompress(data)
        return data

    def _parse_header(self):
        header = struct.unpack(">Iiiii", self.data[:20])
        if header[0] != 0x55AA382D:
            raise ValueError("Not a valid U8 archive")
        return {
            "magic": header[0],
            "root_node_offset": header[1],
            "node_size": header[2],
            "data_offset": header[3],
            "reserved": header[4:8]
        }

    def _parse_nodes(self):
        root_node_offset = self.header["root_node_offset"]
        root_node_data = self.data[root_node_offset:root_node_offset + 12]
        root_node = struct.unpack(">B3sII", root_node_data)
        node_count = root_node[3]  # size_or_next_node_index of the root node

        nodes = []

        for i in range(node_count):
            offset = root_node_offset + i * 12
            node_data = self.data[offset:offset + 12]
            node = struct.unpack(">B3sII", node_data)
            node_type = node[0]
            name_offset = int.from_bytes(node[1], byteorder='big')
            data_offset_or_parent_index = node[2]
            size_or_next_node_index = node[3]
            nodes.append(Node(node_type, name_offset, data_offset_or_parent_index, size_or_next_node_index))

        return nodes

    def _parse_file_names(self):
        node_count = len(self.nodes)
        string_pool_offset = self.header["root_node_offset"] + node_count * 12

        for node in self.nodes:
            name_start = string_pool_offset + node.name_offset
            name_end = self.data.find(b'\x00', name_start)
            node_name = self.data[name_start:name_end].decode('ascii')
            node.set_name(node_name)
    
    def print_nodes(self):
        for node in self.nodes:
            print(node)
    
    def extract_file(self, file_name):
        for node in self.nodes:
            if node.name == file_name:
                start = node.data_offset_or_parent_index
                end = start + node.size_or_next_node_index
                file_data = self.data[start:end]
                
                # Create the full output path in the current working directory
                full_output_path = os.path.join(os.getcwd(), file_name)
                
                with open(full_output_path, 'wb') as f:
                    f.write(file_data)
                print(f"Extracted {file_name} to {full_output_path}")
                return
        print(f"File {file_name} not found in the archive")
