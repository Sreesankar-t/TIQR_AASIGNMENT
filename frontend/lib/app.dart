import 'package:flutter/material.dart';
import './widget/Table2.dart';
import './widget/table1.dart';

class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "sreesankar",
      home: Scaffold(
        body: ListView(
          children: [Table1(), const SizedBox(height: 30), Table2()],
        ),
      ),
    );
  }
}
