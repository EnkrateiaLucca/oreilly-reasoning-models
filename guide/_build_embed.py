import base64, re, pathlib
GUIDE = pathlib.Path('guide/reasoning-training-guide.html')
IMGS = {'grpo':'guide/_img/02_grpo_objective.png','aha':'guide/_img/02_aha_moment.png',
        'aime':'guide/_img/02_aime_curve.png','distill':'guide/_img/02_distillation_table.png'}
def b64(p):
    return 'data:image/png;base64,'+base64.b64encode(pathlib.Path(p).read_bytes()).decode()
entries=',\n'.join(f'  {k}:"{b64(v)}"' for k,v in IMGS.items())
js=('(function(){var M={\n'+entries+'\n};'
    'document.querySelectorAll("[data-paper]").forEach(function(img){'
    'var k=img.getAttribute("data-paper"); if(M[k]) img.src=M[k];});})();')
html=GUIDE.read_text()
html=re.sub(r'(<script id="paperEmbed">).*?(</script>)', lambda m:m.group(1)+js+m.group(2), html, flags=re.S)
GUIDE.write_text(html)
# regenerate artifact body-only variant
style=html[html.index('<style>'):html.index('</style>')+len('</style>')]
body=html[html.index('<body>')+len('<body>'):html.index('</body>')]
pathlib.Path('guide/_artifact_body.html').write_text(style+'\n'+body)
print('injected', len(js), 'bytes of JS; guide=', len(html), 'chars; artifact body=', len(style+body), 'chars')
