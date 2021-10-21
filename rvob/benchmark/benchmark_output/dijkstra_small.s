	.file	"dijkstra_small.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.globl	qHead
	.section	.sbss,"aw",@nobits
	.align	3
	.type	qHead, @object
	.size	qHead, 8
.qHeadV:
	.zero	8
	.comm	AdjMatrix,40000,8
	.globl	g_qCount
	.align	2
	.type	g_qCount, @object
	.size	g_qCount, 4
.g_qCount:
	.zero	4
	.comm	rgnNodes,800,8
	.comm	ch,4,4
	.comm	iPrev,4,4
	.comm	iNode,4,4
	.comm	i,4,4
	.comm	iCost,4,4
	.comm	iDist,4,4
	.section	.rodata
	.align	3
.LC0:
	.string	", %d"
	.text	
	.align	1
	.globl	print_path
	.type	print_path, @function
.print_path:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	sd	a0,-24(s0)
	mv	a5,a1
	sw	a5,-28(s0)
	lw	a5,-28(s0)
	slli	a5,a5,3
	ld	a4,-24(s0)
	add	a5,a4,a5
	lw	a5,4(a5)
	mv	a4,a5
	li	a5,8192
	addi	a5,a5,1807
	beq	a4,a5,.L2
	lw	a5,-28(s0)
	slli	a5,a5,3
	ld	a4,-24(s0)
	add	a5,a4,a5
	lw	a5,4(a5)
	mv	a1,a5
	ld	a0,-24(s0)
	call	print_path
.L2:
	lw	a5,-28(s0)
	mv	a1,a5
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	printf
	lui	a5,%hi(_impure_ptr)
	ld	a5,%lo(_impure_ptr)(a5)
	ld	a5,16(a5)
	mv	a0,a5
	call	fflush
	nop
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	print_path, .-print_path
	.section	.rodata
	.align	3
.LC1:
	.string	"Out, of, memory.
"
	.text	
	.align	1
	.globl	enqueue
	.type	enqueue, @function
.enqueue:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	mv	a5,a0
	mv	a3,a1
	mv	a4,a2
	sw	a5,-36(s0)
	mv	a5,a3
	sw	a5,-40(s0)
	mv	a5,a4
	sw	a5,-44(s0)
	li	a0,24
	call	malloc
	mv	a5,a0
	sd	a5,-32(s0)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	sd	a5,-24(s0)
	ld	a5,-32(s0)
	bne	a5,zero,.L4
	lui	a5,%hi(_impure_ptr)
	ld	a5,%lo(_impure_ptr)(a5)
	ld	a5,24(a5)
	mv	a3,a5
	li	a2,15
	li	a1,1
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	fwrite
	li	a0,1
	call	exit
.L4:
	ld	a5,-32(s0)
	lw	a4,-36(s0)
	sw	a4,0(a5)
	ld	a5,-32(s0)
	lw	a4,-40(s0)
	sw	a4,4(a5)
	ld	a5,-32(s0)
	lw	a4,-44(s0)
	sw	a4,8(a5)
	ld	a5,-32(s0)
	sd	zero,16(a5)
	ld	a5,-24(s0)
	bne	a5,zero,.L7
	lui	a5,%hi(qHead)
	ld	a4,-32(s0)
	sd	a4,%lo(qHead)(a5)
	j	.L6
.L8:
	ld	a5,-24(s0)
	ld	a5,16(a5)
	sd	a5,-24(s0)
.L7:
	ld	a5,-24(s0)
	ld	a5,16(a5)
	bne	a5,zero,.L8
	ld	a5,-24(s0)
	ld	a4,-32(s0)
	sd	a4,16(a5)
.L6:
	lui	a5,%hi(g_qCount)
	lw	a5,%lo(g_qCount)(a5)
	addiw	a5,a5,1
	sext.w	a4,a5
	lui	a5,%hi(g_qCount)
	sw	a4,%lo(g_qCount)(a5)
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	enqueue, .-enqueue
	.align	1
	.globl	dequeue
	.type	dequeue, @function
.dequeue:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	addi	s0,sp,64
	sd	a0,-40(s0)
	sd	a1,-48(s0)
	sd	a2,-56(s0)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	sd	a5,-24(s0)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	beq	a5,zero,.L11
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	lw	a4,4(a5)
	ld	a5,-48(s0)
	sw	a4,0(a5)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	lw	a4,8(a5)
	ld	a5,-56(s0)
	sw	a4,0(a5)
	lui	a5,%hi(qHead)
	ld	a5,%lo(qHead)(a5)
	ld	a4,16(a5)
	lui	a5,%hi(qHead)
	sd	a4,%lo(qHead)(a5)
	ld	a0,-24(s0)
	call	free
	lui	a5,%hi(g_qCount)
	lw	a5,%lo(g_qCount)(a5)
	addiw	a5,a5,-1
	sext.w	a4,a5
	lui	a5,%hi(g_qCount)
	sw	a4,%lo(g_qCount)(a5)
.L11:
	nop
	ld	ra,56(sp)
	ld	s0,48(sp)
	addi	sp,sp,64
	jr	ra
	.size	dequeue, .-dequeue
	.align	1
	.globl	qcount
	.type	qcount, @function
.qcount:
	addi	sp,sp,-16
	sd	s0,8(sp)
	addi	s0,sp,16
	lui	a5,%hi(g_qCount)
	lw	a5,%lo(g_qCount)(a5)
	mv	a0,a5
	ld	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	qcount, .-qcount
	.section	.rodata
	.align	3
.LC2:
	.string	"Shortest, path, is, 0, in, cost., Just, stay, where, you, are."
	.align	3
.LC3:
	.string	"Shortest, path, is, %d, in, cost., "
	.align	3
.LC4:
	.string	"Path, is:, "
	.text	
	.align	1
	.globl	dijkstra
	.type	dijkstra, @function
.dijkstra:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	mv	a5,a0
	mv	a4,a1
	sw	a5,-20(s0)
	mv	a5,a4
	sw	a5,-24(s0)
	lui	a5,%hi(ch)
	sw	zero,%lo(ch)(a5)
	j	.L15
.L16:
	lui	a5,%hi(ch)
	lw	a5,%lo(ch)(a5)
	lui	a4,%hi(rgnNodes)
	addi	a4,a4,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a4,a5
	li	a4,8192
	addi	a4,a4,1807
	sw	a4,0(a5)
	lui	a5,%hi(ch)
	lw	a5,%lo(ch)(a5)
	lui	a4,%hi(rgnNodes)
	addi	a4,a4,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a4,a5
	li	a4,8192
	addi	a4,a4,1807
	sw	a4,4(a5)
	lui	a5,%hi(ch)
	lw	a5,%lo(ch)(a5)
	addiw	a5,a5,1
	sext.w	a4,a5
	lui	a5,%hi(ch)
	sw	a4,%lo(ch)(a5)
.L15:
	lui	a5,%hi(ch)
	lw	a5,%lo(ch)(a5)
	mv	a4,a5
	li	a5,99
	ble	a4,a5,.L16
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	bne	a4,a5,.L17
	lui	a5,%hi(.LC2)
	addi	a0,a5,%lo(.LC2)
	call	puts
	j	.L18
.L17:
	lui	a5,%hi(rgnNodes)
	addi	a4,a5,%lo(rgnNodes)
	lw	a5,-20(s0)
	slli	a5,a5,3
	add	a5,a4,a5
	sw	zero,0(a5)
	lui	a5,%hi(rgnNodes)
	addi	a4,a5,%lo(rgnNodes)
	lw	a5,-20(s0)
	slli	a5,a5,3
	add	a5,a4,a5
	li	a4,8192
	addi	a4,a4,1807
	sw	a4,4(a5)
	lw	a4,-20(s0)
	li	a5,8192
	addi	a2,a5,1807
	li	a1,0
	mv	a0,a4
	call	enqueue
	j	.L19
.L24:
	lui	a5,%hi(iPrev)
	addi	a2,a5,%lo(iPrev)
	lui	a5,%hi(iDist)
	addi	a1,a5,%lo(iDist)
	lui	a5,%hi(iNode)
	addi	a0,a5,%lo(iNode)
	call	dequeue
	lui	a5,%hi(i)
	sw	zero,%lo(i)(a5)
	j	.L20
.L23:
	lui	a5,%hi(iNode)
	lw	a2,%lo(iNode)(a5)
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	lui	a4,%hi(AdjMatrix)
	addi	a4,a4,%lo(AdjMatrix)
	li	a3,100
	mul	a3,a2,a3
	add	a5,a3,a5
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a4,0(a5)
	lui	a5,%hi(iCost)
	sw	a4,%lo(iCost)(a5)
	lui	a5,%hi(iCost)
	lw	a5,%lo(iCost)(a5)
	mv	a4,a5
	li	a5,8192
	addi	a5,a5,1807
	beq	a4,a5,.L21
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	lui	a4,%hi(rgnNodes)
	addi	a4,a4,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a4,a5
	li	a5,8192
	addi	a5,a5,1807
	beq	a4,a5,.L22
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	lui	a4,%hi(rgnNodes)
	addi	a4,a4,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a4,a5
	lw	a3,0(a5)
	lui	a5,%hi(iCost)
	lw	a4,%lo(iCost)(a5)
	lui	a5,%hi(iDist)
	lw	a5,%lo(iDist)(a5)
	addw	a5,a4,a5
	sext.w	a5,a5
	mv	a4,a3
	ble	a4,a5,.L21
.L22:
	lui	a5,%hi(iDist)
	lw	a3,%lo(iDist)(a5)
	lui	a5,%hi(iCost)
	lw	a4,%lo(iCost)(a5)
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	addw	a4,a3,a4
	sext.w	a4,a4
	lui	a3,%hi(rgnNodes)
	addi	a3,a3,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a3,a5
	sw	a4,0(a5)
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	lui	a4,%hi(iNode)
	lw	a4,%lo(iNode)(a4)
	lui	a3,%hi(rgnNodes)
	addi	a3,a3,%lo(rgnNodes)
	slli	a5,a5,3
	add	a5,a3,a5
	sw	a4,4(a5)
	lui	a5,%hi(i)
	lw	a3,%lo(i)(a5)
	lui	a5,%hi(iDist)
	lw	a4,%lo(iDist)(a5)
	lui	a5,%hi(iCost)
	lw	a5,%lo(iCost)(a5)
	addw	a5,a4,a5
	sext.w	a4,a5
	lui	a5,%hi(iNode)
	lw	a5,%lo(iNode)(a5)
	mv	a2,a5
	mv	a1,a4
	mv	a0,a3
	call	enqueue
.L21:
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	addiw	a5,a5,1
	sext.w	a4,a5
	lui	a5,%hi(i)
	sw	a4,%lo(i)(a5)
.L20:
	lui	a5,%hi(i)
	lw	a5,%lo(i)(a5)
	mv	a4,a5
	li	a5,99
	ble	a4,a5,.L23
.L19:
	call	qcount
	mv	a5,a0
	bgt	a5,zero,.L24
	lui	a5,%hi(rgnNodes)
	addi	a4,a5,%lo(rgnNodes)
	lw	a5,-24(s0)
	slli	a5,a5,3
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC3)
	addi	a0,a5,%lo(.LC3)
	call	printf
	lui	a5,%hi(.LC4)
	addi	a0,a5,%lo(.LC4)
	call	printf
	lw	a5,-24(s0)
	mv	a1,a5
	lui	a5,%hi(rgnNodes)
	addi	a0,a5,%lo(rgnNodes)
	call	print_path
	li	a0,10
	call	putchar
.L18:
	nop
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	dijkstra, .-dijkstra
	.section	.rodata
	.align	3
.LC5:
	.string	"r"
	.align	3
.LC6:
	.string	"input.dat"
	.align	3
.LC7:
	.string	"%d"
	.text	
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	addi	s0,sp,64
	mv	a5,a0
	sd	a1,-64(s0)
	sw	a5,-52(s0)
	lui	a5,%hi(.LC5)
	addi	a1,a5,%lo(.LC5)
	lui	a5,%hi(.LC6)
	addi	a0,a5,%lo(.LC6)
	call	fopen
	sd	a0,-32(s0)
	sw	zero,-20(s0)
	j	.L26
.L29:
	sw	zero,-24(s0)
	mulh	s6,s2,s9
	srai	a7,a7,6
	xor	t4,a5,s0
	sll	s7,t6,a5
	mulh	a7,a6,t4
	sra	ra,s8,a6
	mul	s8,t4,s8
	mulhsu	s4,t1,a1
	subw	a6,s1,s8
	srlw	s7,t6,a6
	sll	s1,a5,s8
	slliw	t3,ra,15
	sllw	t4,s0,a4
	j	.L27
.L28:
	addi	a5,s0,-36
	mv	a2,a5
	lui	a5,%hi(.LC7)
	srli	s2,t1,31
	sra	s1,s8,t0
	sltiu	s11,s10,800
	sltu	s2,t3,a2
	mul	s9,a6,a6
	mulhu	a6,s2,s11
	sltiu	s6,a7,1529
	add	s8,ra,t3
	addiw	t4,a1,1710
	sltu	ra,s3,a1
	ori	t5,a3,693
	mv	sp,t4
	srai	s3,a4,19
	sra	a0,a7,a0
	addw	a3,s4,s5
	sraiw	a3,s6,4
	sltu	t6,a2,s8
	mulhsu	t0,a4,a3
	andi	s0,s7,-1444
	srliw	a3,a5,0
	mul	a7,a7,s10
	sraiw	s0,s0,22
	add	a0,t3,t3
	slli	s10,s9,25
	mv	t1,ra
	xor	s2,sp,t6
	srlw	t0,s10,s8
	addi	a1,a5,%lo(.LC7)
	ld	a0,-32(s0)
	call	fscanf
	lw	a4,-36(s0)
	lui	a5,%hi(AdjMatrix)
	addi	a3,a5,%lo(AdjMatrix)
	lw	a5,-24(s0)
	mv	sp,a5
	lw	a1,-20(s0)
	li	a2,100
	mul	a2,a1,a2
	mv	ra,a3
	add	a5,a2,sp
	slli	a5,a5,2
	add	a5,ra,a5
	sw	a4,0(a5)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L27:
	lw	a5,-24(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L28
	lw	a5,-20(s0)
	mv	s11,a5
	mv	ra,s7
	mv	s4,t4
	addiw	a5,s11,1
	srliw	s0,t2,29
	sllw	s9,ra,s6
	and	t5,s5,s5
	mv	sp,s0
	add	t3,sp,a6
	slt	t6,s4,a3
	sllw	s4,s3,sp
	sllw	s0,a7,sp
	slliw	s2,s4,25
	slt	s10,s8,s2
	sraiw	t0,t5,25
	sub	ra,s1,t6
	mul	s11,t2,a0
	mulhsu	t3,s6,s11
	sw	a5,-20(s0)
.L26:
	lw	a5,-20(s0)
	sext.w	a4,a5
	slliw	t1,a2,1
	andi	a3,a5,-1805
	or	a1,a6,a2
	mulh	a1,t3,ra
	srli	s4,a2,22
	slli	s10,s7,30
	mulw	t0,s6,t6
	sra	a7,s6,s4
	slliw	t0,a0,4
	xori	s0,s9,258
	addw	ra,a0,t0
	mulhu	a3,t4,a1
	slt	t3,t6,s11
	li	a5,99
	ble	a4,a5,.L29
	sw	zero,-20(s0)
	li	a5,50
	sraw	s3,s9,s4
	addw	a1,ra,s10
	mv	s0,a7
	sltiu	a3,s11,-1282
	and	s9,s5,s5
	addiw	a0,a4,79
	sll	t2,a6,a3
	srl	s1,s11,s11
	srl	t1,t5,s1
	slli	t2,s1,30
	mv	s2,t5
	add	s9,a1,a1
	slli	t0,s2,3
	sllw	a3,t4,s4
	sw	a5,-24(s0)
	j	.L30
.L31:
	lw	a4,-24(s0)
	li	a5,100
	remw	a5,a4,a5
	sw	a5,-24(s0)
	lw	a4,-24(s0)
	lw	a5,-20(s0)
	mv	a1,a4
	addw	s7,s4,s4
	sra	t6,t0,s11
	mulhsu	s10,s1,s3
	addi	t4,s7,1207
	addw	t6,a7,s4
	srliw	s7,s7,10
	srli	s10,s11,10
	srlw	s10,a3,s2
	sltiu	a2,a3,1101
	sllw	sp,a1,a5
	sltu	a6,a4,s11
	addi	s10,s1,-643
	andi	a2,s0,1330
	mv	a0,a5
	call	dijkstra
	lw	a5,-20(s0)
	addiw	a5,a5,1
	mulhu	s6,a6,a7
	and	ra,t2,s8
	sltiu	s7,a5,599
	sraw	t6,a7,t2
	sltu	s5,a6,a2
	sub	a1,s11,s2
	srli	t6,t0,24
	ori	t5,s1,-259
	mul	s1,s5,a7
	mul	s0,t0,a1
	mulh	a0,s6,a7
	sltu	a2,s9,s5
	sub	s3,s10,sp
	srliw	s0,s2,5
	mulh	s4,s2,t1
	slliw	s10,t6,21
	srliw	t0,s8,29
	ori	t2,s6,1935
	slt	s0,t1,s7
	add	s9,a6,s1
	sltiu	sp,s0,551
	mv	t5,a2
	xori	a0,sp,1572
	ori	s9,s6,-816
	ori	s4,a0,1515
	mul	s5,s8,s5
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	mulhsu	s7,s6,t2
	srliw	a4,s0,2
	srlw	a6,t6,a6
	mv	sp,s5
	slt	a4,a6,t0
	sll	s10,a3,t2
	xor	a3,s3,sp
	srliw	t5,s4,14
	xor	s10,s1,ra
	mulhu	s2,t5,s6
	sltiu	s10,a7,-1985
	addiw	s10,sp,-934
	slt	s2,s9,a4
	sub	t6,ra,t2
	srli	ra,t2,31
	andi	s8,t2,1989
	addw	s11,a7,s9
	slliw	a7,a1,4
	mulhsu	s2,a2,s6
	sub	a6,s4,t0
	sllw	s11,s6,a5
	srai	t1,sp,10
	srai	s8,s6,19
	sllw	s7,a6,a6
	subw	ra,sp,s3
	srl	a3,sp,s0
	sraiw	s6,s6,23
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L30:
	lw	a5,-20(s0)
	sext.w	a4,a5
	li	a5,19
	ble	a4,a5,.L31
	srliw	s4,a4,15
	xori	a2,a2,1492
	sltu	s1,a4,a0
	mv	t6,ra
	addi	s7,a2,1081
	mulh	s4,a1,t6
	mulhu	a1,t1,a4
	xor	s7,a0,a7
	addw	t6,s9,s8
	sltiu	a6,s5,-283
	srlw	s7,a4,t0
	sltu	ra,s11,s6
	slt	s8,t3,t1
	srl	s0,s1,s7
	li	a0,0
	call	exit
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
