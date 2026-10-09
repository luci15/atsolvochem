<?php

	$to = "prashantjagadale@gmail.com";
	$first_name = $_POST['userName']; // required
	$email_from = $_POST['userEmail']; // required
	$telephone = $_POST['userPhone']; // not required
	$comments = $_POST['userMsg']; // required
	$subject = "Inquiry from: $first_name";
	$headers = "sales@atsolvochem.com";



	$body = "\n\n From: $first_name \n\n Email: $email_from \n\n Mobile.no.: $telephone \n\n Inquiry: $comments";

	$sent = mail($to, $subject, $body, $headers) ;

	if($sent)
	{
		echo "<script LANGUAGE='JavaScript'>alert('Email Send Sucessfully !!!!!'); window.location.href = 'contact.html';</script>";
	}
	else
	{
		echo "<script LANGUAGE='JavaScript'>alert('Try again to send email or email us at sales@atsolvochem.com !!!!!'); window.location.href = 'contact.html';</script>";
	}

?>

      