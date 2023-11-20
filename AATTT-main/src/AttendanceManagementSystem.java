import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;
import java.text.DecimalFormat;
import java.util.Vector;

public class AttendanceManagementSystem extends JFrame {
    private JTextField studentNameField;
    private JButton markAttendanceButton;
    private JButton viewPercentageButton;  // New button for viewing attendance percentage
    private JTable attendanceTable;
    private DefaultTableModel tableModel;

    public AttendanceManagementSystem() {
        setTitle("Attendance Management System");
        setSize(600, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel(new BorderLayout());
        add(panel);
        createTopPanel(panel);
        createTablePanel(panel);

        setVisible(true);
    }

    private void createTopPanel(JPanel panel) {
        JPanel topPanel = new JPanel(new FlowLayout());

        JLabel nameLabel = new JLabel("Student Name:");
        studentNameField = new JTextField(20);
        markAttendanceButton = new JButton("Mark Attendance");
        viewPercentageButton = new JButton("View Attendance Percentage");  // New button

        topPanel.add(nameLabel);
        topPanel.add(studentNameField);
        topPanel.add(markAttendanceButton);
        topPanel.add(viewPercentageButton);

        panel.add(topPanel, BorderLayout.NORTH);

        markAttendanceButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                markAttendance();
            }
        });

        viewPercentageButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewAttendancePercentage();
            }
        });
    }

    private void createTablePanel(JPanel panel) {
        tableModel = new DefaultTableModel();
        tableModel.addColumn("ID");
        tableModel.addColumn("Student Name");
        tableModel.addColumn("Attendance Date");

        attendanceTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(attendanceTable);

        panel.add(scrollPane, BorderLayout.CENTER);

        loadAttendanceRecords();
    }

    private void markAttendance() {
        String studentName = studentNameField.getText();

        // Database connection parameters
        String url = "jdbc:mysql://localhost:3306/your_database";
        String username = "root";
        String password = "Mandy@422004";

        try {
            Connection connection = DriverManager.getConnection(url, username, password);

            // Insert attendance record
            String sql = "INSERT INTO attendance (student_name, attendance_date) VALUES (?, CURDATE())";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, studentName);
            preparedStatement.executeUpdate();

            JOptionPane.showMessageDialog(this, "Attendance marked for " + studentName);

            connection.close();

            // Reload attendance records after marking
            loadAttendanceRecords();
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error marking attendance");
        }
    }

    private void loadAttendanceRecords() {
        // Clear existing table data
        tableModel.setRowCount(0);

        // Database connection parameters
        String url = "jdbc:mysql://localhost:3306/your_database";
        String username = "root";
        String password = "Mandy@422004";

        try {
            Connection connection = DriverManager.getConnection(url, username, password);

            // Retrieve attendance records
            String sql = "SELECT * FROM attendance";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);

            // Populate table with attendance records
            while (resultSet.next()) {
                Vector<Object> row = new Vector<>();
                row.add(resultSet.getInt("id"));
                row.add(resultSet.getString("student_name"));
                row.add(resultSet.getDate("attendance_date"));
                tableModel.addRow(row);
            }

            connection.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error loading attendance records");
        }
    }

    private void viewAttendancePercentage() {
        // Database connection parameters
        String url = "jdbc:mysql://localhost:3306/your_database";
        String username = "root";
        String password = "Mandy@422004";

        try {
            Connection connection = DriverManager.getConnection(url, username, password);

            // Count total number of days
            String totalDaysSQL = "SELECT COUNT(DISTINCT attendance_date) AS total_days FROM attendance";
            Statement totalDaysStatement = connection.createStatement();
            ResultSet totalDaysResult = totalDaysStatement.executeQuery(totalDaysSQL);
            totalDaysResult.next();
            int totalDays = totalDaysResult.getInt("total_days");

            // Count attended days for the given student
            String attendedDaysSQL = "SELECT COUNT(DISTINCT attendance_date) AS attended_days " +
                    "FROM attendance WHERE student_name = ?";
            PreparedStatement attendedDaysStatement = connection.prepareStatement(attendedDaysSQL);
            attendedDaysStatement.setString(1, studentNameField.getText());
            ResultSet attendedDaysResult = attendedDaysStatement.executeQuery();
            attendedDaysResult.next();
            int attendedDays = attendedDaysResult.getInt("attended_days");

            // Calculate percentage
            double percentage = ((double) attendedDays / totalDays) * 100;

            DecimalFormat df = new DecimalFormat("#.##");  // Format to two decimal places
            JOptionPane.showMessageDialog(this, "Attendance Percentage: " + df.format(percentage) + "%");

            connection.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error calculating attendance percentage");
        }
    }

    public static void main(String[] args) {
        new AttendanceManagementSystem();
    }
}