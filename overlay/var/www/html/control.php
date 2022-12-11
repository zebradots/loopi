<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/css/pico.min.css">
    <title>loopi | system control</title>
</head>
<body>
<?php

// Perform the requested action

$action = $_GET['action'];
switch ($action) {
	case "restart":
		$status = "Restarting. Please allow at least 60 seconds to reboot.";
		shell_exec('reboot >/dev/null 2>/dev/null &');
		break;
	case "shutdown":
		$status = "Powering off.";
		shell_exec('poweroff >/dev/null 2>/dev/null &');
		break;
}

?>
	<div class="container">
		<article>
			<center>
				<div aria-busy="true"><?php print $status; ?></div>
				<?php if ($action!=='shutdown') { ?>
				<div style="margin-top: 2.5ex;">
					<a role="button" class="outline" href="/">Back to loopi</a>
				</div>
				<?php } ?>
			</center>
		</article>
	</div>
</body>
</html>
