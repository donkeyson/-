#DNA 정제
DNA = []
with open('MC4R_DNA.txt', 'r') as f:
    while True:
        line = f.readline()
        if line.startswith('>'):
            continue
        if not line:
            break
        else:
            DNA.append(line)

#줄 바꿈 제거 함수
def no_linechange(x):
    x = x.replace('\n', '')
    return x

#줄 바꿈 제거하기
i = 0
for dna in DNA:
    DNA[i] = no_linechange(dna)
    i += 1

#한 줄로 바꾸기
DNA_one = ''.join(DNA)

#SNP 정제
SNP = []
with open('SNP.txt', 'r') as f:
   while True:
       line = f.readline()
       SNP.append(line)
       if not line: break

#SNP 줄 바꿈 제거하기, '\t'을 기준으로 분할하기
j = 0
for snp in SNP:
    snp = no_linechange(snp)
    SNP[j] = snp.split('\t')
    j += 1
#마지막 인덱스에 생긴 ['']제거
del SNP[-1]


#테이블 딕셔너리 복사
table = {
'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S',
'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y',
'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I',
'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 'ACC': 'T',
'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K',
'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D',
'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
'GGG': 'G'}

#stop_codons 복사
stop_codons = ['TAA','TAG','TGA']

#문자열 3개씩 나누기, iter함수가 실행될 때마다 다음 인덱스로 넘어가는 성질 이용
#3개로 곱한 값에서 zip함수를 이용해 값을 하나씩 뽑아서 묶기
#map함수를 이용해서 zip으로 묶은 값을 join함수로 하나의 문자열로 만들기
#3개씩 분할된 값을 리스트로 바꾸기
#마지막으로 남은 값 'C'는 별도로 더해주기
split_dna = list(map(''.join, zip(*[iter(DNA_one)]*3)))
split_dna.append('C')

#DNA 염기서열을 구해주는 함수
#s_codon은 바뀌었는데 s_protein이 안 바뀌는 것들이 있음
#함수의 문제가 아니었음 s_protein으로 바꿔도 염기서열이 같은 것들이 있음
def dna_protein(x):
    return_protein = []
    #stop_codons에 속할시 *로 표시
    for dna in x:
        if dna in stop_codons:
            return_protein.append('*')

    #stop_codons에 없으면 테이블 딕셔너리 키값으로 넣기
        elif dna in table.keys():
            return_protein.append(table[dna])

#마지막으로 남은 DNA서열은 '-'로 표시
        else:
            return_protein.append('-')
    return return_protein

#DNA 염기서열 구하기
protein = dna_protein(split_dna)

#SNP 대로 값 바꿔서 구하기 (SNP, 인덱스는 인트형으로 바꾸기)
s_protein = []
#한 줄로 정리한 염기서열 가져오고 리스트로 바꾸기
snp_DNA = list(DNA_one)
for index, snp in SNP:
    #snp를 DNA 염기서열에 적용하기
    #그 단어만 교체해야됨
    snp_DNA[int(index)] = snp
#다시 한 줄로 묶기
snp_DNA = "".join(snp_DNA)

#3개씩 나누기
split_snp_dna = list(map(''.join, zip(*[iter(snp_DNA)]*3)))
split_snp_dna.append('C')

#바뀐 s_protein값 구하기
s_protein = dna_protein(split_snp_dna)


#출력 결과 index, SNP, codon, s_codon, protein, s_protein 순으로 출력
with open('184741_손동희.txt', 'w')as f:
    first_line = 'index\tSNP\tcodon\ts_codon\tprotein\ts_protein\n'
    f.write(first_line)
    for i, j in SNP:
        data = f'{i}\t{j}\t{split_dna[int(i)//3]}\t{split_snp_dna[int(i)//3]}\t\
{protein[int(i)//3]}\t{s_protein[int(i)//3]}\n'
        f.write(data)
