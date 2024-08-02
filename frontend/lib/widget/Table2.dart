import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Table2 extends StatefulWidget {
  @override
  Table2State createState() {
    return Table2State();
  }
}

class Table2State extends State<Table2> {
  List<Map<String, dynamic>> tableData = [];

  @override
  void initState() {
    super.initState();
    readEmployee();
  }

// READ EMPLOYEE
  void readEmployee() async {
    var res = await http.get(Uri.parse('http://10.0.2.2:8080/read-user'));

    List<dynamic> jsonResponse = jsonDecode(res.body);
    setState(() {
      tableData =
          jsonResponse.map((item) => item as Map<String, dynamic>).toList();
    });
  }

// ADD EMPLOYEE
  Future<void> addNewEmployee(
      String name, String age, String department) async {
    Map<String, dynamic> data = {
      "name": name,
      "age": age,
      "department": department,
    };

    try {
      await http.post(
        Uri.parse('http://10.0.2.2:8080/add-user'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(data),
      );

      readEmployee();
    } catch (e) {
      print('Error occurred: $e');
    }
  }

  // UDATE EMPLOYEE
  void updateEmployee(String name, String department, String age, id) async {
    Map<String, dynamic> data = {
      "name": name,
      "department": department,
      "age": age
    };

    try {
      await http.put(
        Uri.parse("http://10.0.2.2:8080/update-employee/$id"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(data),
      );

      readEmployee();
    } catch (e) {}
  }

// DELETE EMPLOYEE
  void deleteEmployee(int id) async {
    try {
      await http.delete(Uri.parse("http://10.0.2.2:8080/delete-user/$id"));
      readEmployee();
    } catch (e) {
      print(e);
    }
  }

// MODAL
  void showFormDialog({required bool isEditing, int? id}) {
    final TextEditingController nameController = TextEditingController();
    final TextEditingController ageController = TextEditingController();
    final TextEditingController departmentController = TextEditingController();

    if (isEditing) {
      final item = tableData.firstWhere((item) => item['id'] == id);
      nameController.text = item['name'];
      ageController.text = item['age'];
      departmentController.text = item['department'];
    }

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(isEditing ? 'Edit employee' : 'Create New Employee'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: nameController,
                  decoration:
                      const InputDecoration(labelText: 'Department Name'),
                ),
                TextField(
                  controller: ageController,
                  decoration: const InputDecoration(labelText: 'Age'),
                ),
                TextField(
                  controller: departmentController,
                  decoration: const InputDecoration(labelText: 'Department'),
                ),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Cancel'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: Text(isEditing ? 'Save' : 'Create'),
              onPressed: () {
                if (isEditing) {
                  updateEmployee(nameController.text, departmentController.text,
                      ageController.text, id);
                } else {
                  addNewEmployee(nameController.text, ageController.text,
                      departmentController.text);
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
      child: Column(
        children: [
          TextButton(
            onPressed: () {
              showFormDialog(isEditing: false);
            },
            style: TextButton.styleFrom(
              backgroundColor: Color.fromARGB(255, 20, 7, 94),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5),
              ),
            ),
            child: const Text("Create employee"),
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
            columns: <DataColumn>[
              // DataColumn(label: Text("ID")),
              const DataColumn(label: Text("Name")),

              const DataColumn(label: Text("Department")),

              DataColumn(
                label: Container(
                  width: 10,
                  child: const Text("Age"),
                ),
              ),

              const DataColumn(label: Text("Action")),
            ],
            rows: tableData.map<DataRow>((data) {
              return DataRow(
                cells: <DataCell>[
                  // DataCell(Text(data['id'].toString())),
                  DataCell(Text(data['name'])),
                  DataCell(Text(data['department'])),
                  DataCell(Text(data['age'])),
                  DataCell(Row(
                    children: <Widget>[
                      IconButton(
                        icon: const Icon(Icons.edit),
                        color: Colors.teal,
                        onPressed: () {
                          showFormDialog(isEditing: true, id: data['id']);
                        },
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete),
                        color: Colors.red,
                        onPressed: () {
                          deleteEmployee(data['id']);
                        },
                      ),
                    ],
                  )),
                ],
              );
            }).toList(),
          )
        ],
      ),
    );
  }
}
