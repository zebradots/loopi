<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="300">
    <link rel="stylesheet" href="/css/pico.min.css">
    <title>loopi | main</title>
</head>
<?php

function ago($s) {
	$from = new DateTime("@0");
	$to = new DateTime("@$s");
	return $from->diff($to)->format('%a days, %h hours, and %i minutes');
}

$manage_url = "/media/";
$current = `pgrep -a omxplayer.bin | awk '{print $NF}'`;
if ($current=='') {
	$status = "No media playing. Want to <a href='$manage_url' target='_manage'><strong>upload a video</strong></a>?";
	$busy = false;
} else {
	$pid = `pidof omxplayer.bin`;
	$start = intval(`stat --format=%Y /proc/$pid`);	
	$now = time();
	$started = $start;
	$playtime = ago($now - $started);
	$status = "Playing <strong>".trim(basename($current))."</strong>. Looped for $playtime.";
	$busy = true;
}
?>
<body>
	<header style="padding-bottom: 0;">
		<div class="container headings">
			<h1><img src="/assets/loopi.svg" style="max-height: 10vh; max-width: 50vw;"></h1>
			<h2>Seamless looped video playback</h2>
		</div>
	</header>
	<div class="container">
		<center>
			<article>
				<?=($busy?"<p aria-busy='true'></p>":"");?>
				<div>
					<?=$status;?>
				</div>
			</article>
		</center>
	</div>
	<div class="container">
		<div class="grid">
			<div>
				<button id="manage" class="outline">Manage media</button>
			</div>
			<div>
				<button id="restart" class="outline">Restart</button>
			</div>
			<div>
				<button id="shutdown" class="outline">Shutdown</button>
			</div>
		</div>
	</div>
	<script>
	document.getElementById("manage").onclick = function manage() {
		window.open("<?=$manage_url;?>");
	}
	document.getElementById("restart").onclick = function restart() {
		location.href = "/control.php?action=restart";
	}
	document.getElementById("shutdown").onclick = function shutdown() {
		location.href = "/control.php?action=shutdown";
	}
	</script>
</body>
</html>
