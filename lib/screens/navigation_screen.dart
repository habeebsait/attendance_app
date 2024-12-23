import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LocationTimeScreen extends StatefulWidget {
  @override
  _LocationTimeScreenState createState() => _LocationTimeScreenState();
}

class _LocationTimeScreenState extends State<LocationTimeScreen> {
  final TextEditingController originController = TextEditingController();
  String eta = "";
  bool isLoading = false;

  Future<void> getETA(String origin) async {
    setState(() {
      isLoading = true;
      eta = "";
    });

    try {
      final apiKey = "";
      final destination = "Ramaiah Institute of Technology, Bangalore, India";
      final url =
          "https://maps.googleapis.com/maps/api/directions/json?origin=${Uri.encodeFull(origin)}&destination=${Uri.encodeFull(destination)}&key=$apiKey";

      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['routes'] != null && data['routes'].isNotEmpty) {
          final legs = data['routes'][0]['legs'];
          if (legs != null && legs.isNotEmpty) {
            final duration = legs[0]['duration']['text'];
            final distance = legs[0]['distance']['text'];
            setState(() {
              eta = "Duration: $duration\nDistance: $distance";
            });
          } else {
            setState(() {
              eta = "No route found";
            });
          }
        } else {
          setState(() {
            eta = "No routes available";
          });
        }
      } else {
        setState(() {
          eta = "Failed to fetch data";
        });
      }
    } catch (e) {
      setState(() {
        eta = "Error occurred while fetching ETA";
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.teal.shade700, Colors.teal.shade900],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // App Bar with Back Button
              Container(
                padding: EdgeInsets.all(16),
                child: Row(
                  children: [
                    // Back Button
                    InkWell(
                      onTap: () => Navigator.of(context).pop(),
                      child: Container(
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Icon(
                          Icons.arrow_back_ios_new,
                          color: Colors.white,
                          size: 20,
                        ),
                      ),
                    ),
                    SizedBox(width: 12),
                    Icon(Icons.location_on, color: Colors.white, size: 30),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        "RIT Campus Navigator",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              Expanded(
                child: Container(
                  margin: EdgeInsets.only(top: 20),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(30),
                      topRight: Radius.circular(30),
                    ),
                  ),
                  child: SingleChildScrollView(
                    padding: EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Destination",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w500,
                            color: Colors.grey[600],
                          ),
                        ),
                        SizedBox(height: 8),
                        Container(
                          padding: EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.teal.shade50,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            children: [
                              Icon(Icons.school, color: Colors.teal),
                              SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  "Ramaiah Institute of Technology\nBangalore, India",
                                  style: TextStyle(
                                    fontSize: 16,
                                    color: Colors.teal.shade700,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(height: 24),
                        Text(
                          "Your Location",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w500,
                            color: Colors.grey[600],
                          ),
                        ),
                        SizedBox(height: 8),
                        TextField(
                          controller: originController,
                          decoration: InputDecoration(
                            hintText: 'Enter your starting location',
                            prefixIcon: Icon(Icons.search, color: Colors.teal),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide:
                                  BorderSide(color: Colors.teal.shade200),
                            ),
                            focusedBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide:
                                  BorderSide(color: Colors.teal, width: 2),
                            ),
                            filled: true,
                            fillColor: Colors.grey.shade50,
                          ),
                        ),
                        SizedBox(height: 24),
                        SizedBox(
                          width: double.infinity,
                          height: 50,
                          child: ElevatedButton(
                            onPressed: () {
                              if (originController.text.isNotEmpty) {
                                getETA(originController.text);
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.teal,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            child: isLoading
                                ? CircularProgressIndicator(color: Colors.white)
                                : Text(
                                    "Calculate Route",
                                    style: TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                          ),
                        ),
                        SizedBox(height: 24),
                        if (eta.isNotEmpty)
                          Container(
                            padding: EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.teal.shade50,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: Colors.teal.shade200),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  "Route Information",
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.teal.shade700,
                                  ),
                                ),
                                SizedBox(height: 8),
                                Text(
                                  eta,
                                  style: TextStyle(
                                    fontSize: 16,
                                    color: Colors.teal.shade900,
                                  ),
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
