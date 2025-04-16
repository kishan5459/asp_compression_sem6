document.getElementById('uploadForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const form = new FormData();
  const fileInput = document.getElementById('imageInput');
  form.append('image', fileInput.files[0]);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/compress', true);

  const progress = document.querySelector('.progress');
  const bar = document.getElementById('bar');
  progress.style.display = 'block';
  bar.style.width = '0%';

  xhr.upload.onprogress = function (e) {
      if (e.lengthComputable) {
          let percent = (e.loaded / e.total) * 100;
          bar.style.width = percent + '%';
      }
  };

  xhr.onload = function () {
      if (xhr.status === 200) {
          const res = JSON.parse(xhr.responseText);
          document.getElementById('origSize').textContent = res.original_size_kb;
          document.getElementById('compSize').textContent = res.compressed_size_kb;
          document.getElementById('ratio').textContent = res.compression_ratio;

          const downloadLink = document.getElementById('downloadLink');
          downloadLink.href = '/download/' + res.output_file;
          downloadLink.style.display = 'inline-block';

          downloadLink.onclick = () => {
              setTimeout(() => {
                  document.getElementById('uploadForm').reset();
                  document.getElementById('result').style.display = 'none';
                  progress.style.display = 'none';
                  bar.style.width = '0%';
              }, 1000); // Give time for download before UI reset
          };

          document.getElementById('result').style.display = 'block';
      } else {
          alert('Compression failed. Please try again.');
      }
      bar.style.width = '100%';
  };

  xhr.send(form);
});
