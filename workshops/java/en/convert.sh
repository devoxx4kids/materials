# Install asciidoctor as "sudo gem install asciidoctor"
echo "Converting to HTML ..."
asciidoctor -a toc -a numbered java.adoc
echo "done"
