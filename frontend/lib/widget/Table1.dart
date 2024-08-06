import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Table1 extends StatefulWidget {
  @override
  Table1State createState() => Table1State();
}

class Table1State extends State<Table1> {
  List<Map<String, dynamic>> tableData = [];

  @override
  void initState() {
    super.initState();
    readDepartment();
  }

// READ DEPAERMENT
  void readDepartment() async {
    try {
      var res =
          await http.get(Uri.parse('http://10.0.2.2:8000/read-department'));

      List<dynamic> jsonResponse = jsonDecode(res.body);
      setState(() {
        tableData =
            jsonResponse.map((item) => item as Map<String, dynamic>).toList();
      });
    } catch (e) {
      print(e);
    }
  }

// ADD DEPARTMENT
  Future<void> addDepartment(String name) async {
    Map<String, dynamic> data = {
      'name': name,
      "number_of_employee": 0,
    };

    try {
      var res = await http.post(
          Uri.parse("http://10.0.2.2:8000/add-department"),
          headers: {"Content-Type": "application/json"},
          body: jsonEncode(data));
      print(res.body);
      readDepartment();
    } catch (e) {
      print(e);
    }
  }

// UDATE DEPARTMENT
  void updateDepartment(String name, id) async {
    Map<String, dynamic> data = {
      "name": name,
    };

    try {
      await http.put(
        Uri.parse("http://10.0.2.2:8000/update-department/$id"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(data),
      );

      readDepartment();
    } catch (e) {}
  }

// DELETE DEPARTMENT
  void deleteDepartment(int id) async {
    final item = tableData.firstWhere((item) => item['id'] == id);

    if (item['number_of_employee'] == 0) {
      try {
        await http
            .delete(Uri.parse('http://10.0.2.2:8000/delete-department/$id'));

        readDepartment();
      } catch (e) {
        print(e);
      }
    } else {
      const snackBar = SnackBar(
        content:
            Text('Cannot delete the department. There are employees here.'),
      );
      ScaffoldMessenger.of(context).showSnackBar(snackBar);
    }
  }

  void showFormDialog({required bool isEditing, int? itemId}) {
    final TextEditingController nameController = TextEditingController();

    if (isEditing) {
      final item = tableData.firstWhere((element) => element['id'] == itemId);
      nameController.text = item['name'];
    }

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(isEditing ? 'Edit Department' : 'Create New Department'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Department Name'),
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              child: Text('Cancel'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: Text(isEditing ? 'Save' : 'Create'),
              onPressed: () {
                if (isEditing) {
                  updateDepartment(nameController.text, itemId);
                } else {
                  addDepartment(nameController.text);
                }
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(top: 20),
      child: Column(
        children: [
          TextButton(
            onPressed: () {
              showFormDialog(isEditing: false);
            },
            style: TextButton.styleFrom(
              backgroundColor: const Color.fromARGB(255, 20, 7, 94),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5),
              ),
            ),
            child: const Text("Create new Department"),
          ),
          DataTable(
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(width: 2.0, color: Colors.lightBlue.shade900),
                bottom:
                    BorderSide(width: 2.0, color: Colors.lightBlue.shade900),
                left: BorderSide(width: 2.0, color: Colors.lightBlue.shade900),
                right: BorderSide(width: 2.0, color: Colors.lightBlue.shade900),
              ),
            ),
            columns: const <DataColumn>[
              DataColumn(
                label: Text('ID'),
              ),
              DataColumn(
                label: Text('Name'),
              ),
              DataColumn(
                label: Text('Emp'),
              ),
              DataColumn(
                label: Text('Action'),
              ),
            ],
            rows: tableData.map<DataRow>((data) {
              return DataRow(
                cells: <DataCell>[
                  DataCell(Text(data['id'].toString())),
                  DataCell(Text(data['name'])),
                  DataCell(Text(data['number_of_employee'].toString())),
                  DataCell(Row(
                    children: <Widget>[
                      IconButton(
                        icon: Icon(Icons.edit),
                        color: Colors.teal,
                        onPressed: () {
                          showFormDialog(isEditing: true, itemId: data['id']);
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        color: Colors.red,
                        onPressed: () {
                          deleteDepartment(data['id']);
                        },
                      ),
                    ],
                  )),
                ],
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
